from __future__ import annotations

import time
import re

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.rate_limit import check_rate_limit
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import Account, Role
from app.dependencies import get_current_jwt, get_db, redis_client
from app.schemas.auth import (
    Credentials,
    RegisterPayload,
    RoleSelection,
    TokenResponse,
    AdminTokenRequest,
    MultiRoleResponse,
)

router = APIRouter(prefix="", tags=["auth"])
bearer_scheme = HTTPBearer(auto_error=False)


async def fetch_roles_by_codes(db: AsyncSession, codes: list[int]) -> list[Role]:
    """Получить модели ролей по их числовым кодам."""
    if not codes:
        return []
    rows = (await db.scalars(select(Role).where(Role.code.in_(codes)))).all()
    return list(rows)


@router.post("/register", status_code=201)
async def register(payload: RegisterPayload, db: AsyncSession = Depends(get_db)) -> dict:
    """Создать аккаунт и привязать роли."""
    exists = await db.scalar(select(Account).where(Account.login == payload.login))
    if exists:
        raise HTTPException(status_code=409, detail="Логин уже существует")

    raw_roles = payload.roles or ""
    try:
        parsed_codes = [
            int(code)
            for code in re.split(r"[\s,;]+", raw_roles)
            if code.strip()
        ]
    except ValueError:
        raise HTTPException(status_code=400, detail="Роли должны содержать целые числа") from None

    roles = await fetch_roles_by_codes(db, parsed_codes)
    requested = set(parsed_codes)
    resolved = {role.code for role in roles}
    missing = sorted(requested - resolved)
    if missing:
        raise HTTPException(status_code=400, detail=f"Неизвестные коды ролей: {missing}")

    account = Account(
        login=payload.login,
        password_hash=hash_password(payload.password),
        roles=roles,
    )
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return {"id": account.id, "roles": account.roles_codes()}


async def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    """Убедитесь, что вызывающий абонент предоставил токен администратора (код роли 1)."""
    if not credentials or credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Заголовок авторизации должен содержать токен Bearer")

    claims = await get_current_jwt(credentials.credentials)
    role_code = int(claims.get("role", 0))
    if role_code != 1:
        raise HTTPException(status_code=403, detail="Требуются права администратора")
    return claims


@router.post(
    "/auth",
    status_code=200,
    response_model=TokenResponse | MultiRoleResponse,
)
async def auth(
    credentials: Credentials,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse | MultiRoleResponse:
    """Аутентификация по логину/паролю и выбор роли, если она назначена"""
    await check_rate_limit(redis_client, request, credentials.login)

    account = await db.scalar(select(Account).where(Account.login == credentials.login))
    if not account or not verify_password(credentials.password, account.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    codes = account.roles_codes()
    real_roles = [code for code in codes if code != 0]
    if not real_roles:
        token = create_access_token(subject=account.login, role=0)
        await redis_client.setex(
            f"active:{token['jti']}",
            settings.access_token_expires_min * 60,
            account.login,
        )
        return TokenResponse(access_token=token["access_token"], role=0)

    if len(real_roles) > 1:
        # Возвращаем 204 и JSON со списком ролей для выбора пользователем.
        return JSONResponse(status_code=204, content={"roles": real_roles})


    chosen = real_roles[0]
    token = create_access_token(subject=account.login, role=chosen)
    await redis_client.setex(
        f"active:{token['jti']}",
        settings.access_token_expires_min * 60,
        account.login,
    )
    return TokenResponse(access_token=token["access_token"], role=chosen)


@router.post("/authentication", status_code=200)
async def authentication_select(
    payload: RoleSelection,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Выдать JWT для конкретной роли после подтверждения пароля."""
    await check_rate_limit(redis_client, request, payload.login)

    account = await db.scalar(select(Account).where(Account.login == payload.login))
    if not account or not verify_password(payload.password, account.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    if payload.role not in account.roles_codes():
        raise HTTPException(status_code=403, detail="Роль не назначена этой учетной записи")

    token = create_access_token(subject=account.login, role=payload.role)
    await redis_client.setex(
        f"active:{token['jti']}",
        settings.access_token_expires_min * 60,
        account.login,
    )
    return TokenResponse(access_token=token["access_token"], role=payload.role)


@router.get("/authentication", status_code=200, response_model=int)
async def authentication_current(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> int:
    """Вернуть код роли, хранящийся в токене Bearer."""
    if not credentials or credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Заголовок авторизации должен содержать токен Bearer")

    claims = await get_current_jwt(credentials.credentials)
    return int(claims.get("role", 0))


@router.post("/admin/token", status_code=200, response_model=TokenResponse)
async def admin_issue_token(
    payload: AdminTokenRequest,
    _: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Выпустить новый токен для пользователя от имени администратора."""
    account = await db.scalar(select(Account).where(Account.login == payload.login))
    if not account:
        raise HTTPException(status_code=404, detail="Аккаунт не найден")

    if payload.role == 1:
        raise HTTPException(status_code=403, detail="Невозможно выдать токены администратора")

    if payload.role not in account.roles_codes():
        raise HTTPException(status_code=403, detail="У пользователя нет запрошенной роли")

    token = create_access_token(subject=account.login, role=payload.role)
    await redis_client.setex(
        f"active:{token['jti']}",
        settings.access_token_expires_min * 60,
        account.login,
    )
    return TokenResponse(access_token=token["access_token"], role=payload.role)


@router.post(
    "/logout",
    status_code=204,
    response_model=None,
)
async def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> None:
    """Отозвать активный JWT, сохранив его jti в Redis."""
    if not credentials or credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Заголовок авторизации должен содержать токен Bearer")

    claims = await get_current_jwt(credentials.credentials)
    jti = claims.get("jti")
    exp = int(claims.get("exp", 0))
    ttl = max(exp - int(time.time()), 0)

    if jti and ttl > 0:
        await redis_client.setex(f"revoked:{jti}", ttl, "1")


ROLE_TITLES = {
    0: "без роли",
    1: "администратор",
    2: "HR",
    3: "университет",
    4: "студент",
}


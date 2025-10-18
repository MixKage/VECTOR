from __future__ import annotations

from typing import AsyncGenerator

from fastapi import HTTPException
from jose import JWTError, jwt
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import SessionLocal

# Общий асинхронный клиент Redis для ограничения скорости и управления токенами.
redis_client = Redis.from_url(settings.redis_url, decode_responses=True)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает асинхронную сессию SQLAlchemy для области запроса."""
    async with SessionLocal() as session:
        yield session


async def get_current_jwt(token: str) -> dict:
    """Декодирует полезную нагрузку JWT и проверяет, что токен не был аннулирован."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Недействительный токен") from None

    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=401, detail="Отсутствует jti токена")

    revoked = await redis_client.get(f"revoked:{jti}")
    if revoked:
        raise HTTPException(status_code=401, detail="Токен аннулирован")

    return payload

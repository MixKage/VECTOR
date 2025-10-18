from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from jose import jwt
from passlib.context import CryptContext
import uuid

from app.core.config import settings

# Контекст для хеширования паролей с использованием схемы bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: str, role: int, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Создаёт подписанный JWT-токен доступа с `jti` для аннулирования.

    Аргументы:
        subject: Основной субъект (логин), сохраняемый в заявке `sub`.
        role: Целочисленное значение роли (0..4).
        extra: Дополнительные необязательные заявления.

    Возвращает:
        Словарь, содержащий строку токена, jti и дату истечения.
    """
    now = datetime.now(timezone.utc)  # Текущая дата и время в UTC
    expire = now + timedelta(minutes=settings.access_token_expires_min)  # Дата истечения токена
    jti = str(uuid.uuid4())  # Генерация уникального идентификатора для токена

    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),  # Время создания токена
        "exp": int(expire.timestamp()),  # Время истечения токена
        "jti": jti,
        "role": role,
    }
    if extra:
        payload.update(extra)  # Дополнительные заявления, если есть

    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)  # Подписание токена
    return {"access_token": token, "jti": jti, "exp": expire}  # Возвращение токена и его метаданных

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль по сравнению с хешем bcrypt с использованием Passlib."""
    return pwd_context.verify(plain_password, hashed_password)  # Возвращает True, если пароль правильный

def hash_password(password: str) -> str:
    """Хеширует пароль с использованием bcrypt через Passlib."""
    return pwd_context.hash(password)  # Возвращает хешированный пароль

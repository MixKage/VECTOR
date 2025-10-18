from __future__ import annotations
from pydantic import BaseModel
import os

class Settings(BaseModel):
    """Настройки приложения, загружаемые из переменных окружения.

    Атрибуты:
        database_url: Асинхронный SQLAlchemy URL базы данных для PostgreSQL.
        redis_url: URL подключения к Redis.
        jwt_secret: Секрет, используемый для подписания JWT.
        jwt_algorithm: Алгоритм, используемый для подписания JWT.
        access_token_expires_min: Время жизни токена доступа в минутах.
        rate_limit_window_sec: Время окна ограничения скорости в секундах.
        rate_limit_max_hits: Максимальное количество запросов за окно.
    """
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/authdb")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    jwt_secret: str = os.getenv("JWT_SECRET", "change_me")
    jwt_algorithm: str = os.getenv("JWT_ALG", "HS256")
    access_token_expires_min: int = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", "60"))

    rate_limit_window_sec: int = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "60"))
    rate_limit_max_hits: int = int(os.getenv("RATE_LIMIT_MAX_HITS", "10"))

settings = Settings()

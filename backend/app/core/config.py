"""Конфигурация приложения на основе Pydantic Settings."""

from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Централизованные настройки приложения, загружаемые из переменных окружения."""

    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(..., env="REDIS_URL")
    app_name: str = Field("Vacancies API", env="APP_NAME")
    frontend_origins_raw: str = Field(
        "http://localhost:3000,http://127.0.0.1:3000,http://frontend",
        env="FRONTEND_ORIGINS",
    )

    @property
    def frontend_origins(self) -> List[str]:
        """Получить список разрешённых Origins."""
        return [origin.strip() for origin in self.frontend_origins_raw.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Вернуть кэшированный экземпляр настроек."""
    return Settings()


settings = get_settings()

"""Конфигурация приложения на основе Pydantic Settings."""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Централизованные настройки приложения, загружаемые из переменных окружения."""

    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(..., env="REDIS_URL")
    app_name: str = Field("Vacancies API", env="APP_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Вернуть кэшированный экземпляр настроек."""
    return Settings()


settings = get_settings()

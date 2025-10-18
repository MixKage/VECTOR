"""Точка входа приложения."""

from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(api_router)


@app.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    """Простой эндпоинт для проверки доступности сервиса."""
    return {"status": "ok"}

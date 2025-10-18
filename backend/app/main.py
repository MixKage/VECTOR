from __future__ import annotations
from fastapi import FastAPI

from app.db.session import engine, Base
from app.routers import auth as auth_router
from app.routers import crud as crud_router

# Создание экземпляра FastAPI с названием и версией приложения
app = FastAPI(title="Auth API", version="0.1.0")

@app.on_event("startup")
async def on_startup() -> None:
    """Создаёт таблицы, если они не существуют (для разработки). Используйте Alembic в продакшене."""
    async with engine.begin() as conn:
        # Запуск синхронного создания всех таблиц в БД
        await conn.run_sync(Base.metadata.create_all)

# Подключение маршрутизаторов для аутентификации и CRUD операций
app.include_router(auth_router.router)
app.include_router(crud_router.router)

"""Конфигурация движка и сессии базы данных."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.db.base import Base


engine = create_async_engine(settings.database_url, echo=False, future=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Отдать асинхронную сессию SQLAlchemy в рамках запроса."""
    async with async_session_factory() as session:
        yield session


__all__ = ["engine", "async_session_factory", "get_db", "Base"]

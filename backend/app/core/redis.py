"""Подключение к Redis и вспомогательные функции кэширования."""

from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any

from redis.asyncio import Redis

from app.core.config import settings

redis_client = Redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
)


def _json_default(value: Any) -> str:
    """Сериализатор для объектов, которые не понимает json.dumps."""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError(f"Неизвестный тип для сериализации: {type(value)!r}")


async def get_cache(key: str) -> Any | None:
    """Получить значение из Redis и декодировать JSON."""
    payload = await redis_client.get(key)
    if payload is None:
        return None
    return json.loads(payload)


async def set_cache(key: str, value: Any, expire_seconds: int = 300) -> None:
    """Сохранить значение в Redis с автоматической сериализацией в JSON."""
    await redis_client.set(key, json.dumps(value, default=_json_default), ex=expire_seconds)


async def delete_by_pattern(pattern: str) -> None:
    """Удалить ключи, подходящие под указанный шаблон."""
    async for key in redis_client.scan_iter(match=pattern):
        await redis_client.delete(key)


__all__ = ["redis_client", "get_cache", "set_cache", "delete_by_pattern"]

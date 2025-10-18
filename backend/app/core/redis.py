"""Утилиты работы с Redis: кэш, счётчики, списки."""

from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any, Sequence

from redis.asyncio import Redis

from app.core.config import settings

redis_client = Redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
)


def _json_default(value: Any) -> str:
    """Поддержка сериализации дат и дат с временем в JSON."""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError(f"Неизвестный тип для сериализации: {type(value)!r}")


async def get_cache(key: str) -> Any | None:
    """Вернуть значение по ключу и десериализовать из JSON."""
    payload = await redis_client.get(key)
    if payload is None:
        return None
    return json.loads(payload)


async def set_cache(key: str, value: Any, expire_seconds: int = 300) -> None:
    """Сохранить значение с TTL и сериализацией в JSON."""
    await redis_client.set(key, json.dumps(value, default=_json_default), ex=expire_seconds)


async def delete_by_pattern(pattern: str) -> None:
    """Удалить все ключи, удовлетворяющие шаблону."""
    async for key in redis_client.scan_iter(match=pattern):
        await redis_client.delete(key)


async def increment_counter(key: str, amount: int = 1) -> int:
    """Увеличить числовой счётчик и вернуть новое значение."""
    return int(await redis_client.incrby(key, amount))


async def push_recent(key: str, value: Any, max_length: int = 50) -> None:
    """Добавить элемент в начало списка, ограничив его длину."""
    await redis_client.lpush(key, json.dumps(value, default=_json_default))
    await redis_client.ltrim(key, 0, max_length - 1)


async def get_recent(key: str, limit: int = 10) -> Sequence[Any]:
    """Получить последние элементы списка, восстановив объекты из JSON."""
    raw_items = await redis_client.lrange(key, 0, limit - 1)
    return [json.loads(item) for item in raw_items]


__all__ = [
    "redis_client",
    "get_cache",
    "set_cache",
    "delete_by_pattern",
    "increment_counter",
    "push_recent",
    "get_recent",
]


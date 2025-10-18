from __future__ import annotations

from fastapi import HTTPException, Request
from redis.asyncio import Redis

from app.core.config import settings

AUTH_BUCKET_PREFIX = "rl:auth:"


async def check_rate_limit(redis: Redis, request: Request, key_part: str) -> None:
    """Simple fixed-window rate limit using Redis INCR + EXPIRE."""
    client_ip = request.client.host if request.client else "unknown"
    key = f"{AUTH_BUCKET_PREFIX}{client_ip}:{key_part}"

    hits = await redis.incr(key)
    if hits == 1:
        await redis.expire(key, settings.rate_limit_window_sec)
    if hits > settings.rate_limit_max_hits:
        ttl = await redis.ttl(key)
        raise HTTPException(status_code=429, detail=f"Too many attempts. Retry in {ttl}s")

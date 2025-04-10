from typing import AsyncIterator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis.asyncio import Redis


async def init_redis_pool(host: str, port: int, password: str = "") -> AsyncIterator[Redis]:
    # session = Redis.from_url(f"redis://{host}", password=password, encoding="utf-8", decode_responses=True)
    session = Redis.from_url(f"redis://{host}:{port}/0", encoding="utf-8", decode_responses=True)

    FastAPICache.init(RedisBackend(session), prefix="fastapi-cache")
    yield session
    session.close()
    await session.wait_closed()

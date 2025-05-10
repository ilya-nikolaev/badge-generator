import logging

import redis.asyncio as redis

from badge_gen.cache.base import Cacher

logger = logging.getLogger(__name__)


class RedisCacher(Cacher):
    def __init__(self, client: redis.Redis, ttl: int = 600):
        self.client = client
        self.ttl = ttl

    async def save(self, key: str, value: str) -> None:
        try:
            await self.client.setex(key, self.ttl, value)
        except redis.RedisError:
            logger.error("Cache save failed")

    async def load(self, key: str) -> str | None:
        try:
            response: bytes | None = await self.client.get(key)
            return response.decode() if response is not None else None
        except redis.RedisError:
            logger.error("Cache load failed")

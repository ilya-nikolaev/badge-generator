import logging

import redis.asyncio as redis

from badge_gen.cachers.base import Cacher

logger = logging.getLogger(__name__)


class RedisCacher(Cacher):
    def __init__(self, client: redis.Redis, ttl: int = 600):
        self.client = client
        self.ttl = ttl

    async def _save(self, key: str, value: str) -> None:
        try:
            await self.client.setex(key, self.ttl, value)
        except redis.RedisError:
            logger.exception("Cache save failed")
        else:
            logger.debug("Cache saved: %s", key)

    async def _load(self, key: str) -> str | None:
        try:
            response: bytes | None = await self.client.get(key)
        except redis.RedisError:
            logger.exception("Cache load failed")
            return None

        if response is not None:
            logger.debug("Cache loaded: %s", key)
            return response.decode()

        return None

from collections.abc import AsyncIterable

import httpx
import redis.asyncio as redis
from dishka import Provider, Scope, from_context, provide
from jinja2 import BaseLoader, Environment, FileSystemLoader

from badge_gen.cache.base import Cacher
from badge_gen.cache.redis import RedisCacher
from badge_gen.main.config import Config


class TemplateProvider(Provider):
    config = from_context(Config, scope=Scope.APP)

    @provide(scope=Scope.APP, provides=BaseLoader)
    def get_loader(self, config: Config) -> FileSystemLoader:
        return FileSystemLoader(config.template.path)

    @provide(scope=Scope.APP)
    def get_env(self, loader: BaseLoader) -> Environment:
        env = Environment(loader=loader)
        env.filters["pad"] = lambda val, width: f"{int(val):0{width}d}"
        return env


class HTTPProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_http_client(self) -> AsyncIterable[httpx.AsyncClient]:
        async with httpx.AsyncClient() as client:
            yield client


class CacheProvider(Provider):
    config = from_context(Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_redis_pool(
        self, config: Config
    ) -> AsyncIterable[redis.ConnectionPool]:
        pool = redis.ConnectionPool.from_url(config.cache.redis_uri)
        yield pool
        await pool.aclose()

    @provide(scope=Scope.REQUEST)
    async def get_redis_client(
        self, pool: redis.ConnectionPool
    ) -> AsyncIterable[redis.Redis]:
        connection = redis.Redis.from_pool(pool)
        yield connection
        await connection.aclose()

    @provide(scope=Scope.REQUEST, provides=Cacher)
    async def get_redis_cacher(self, client: redis.Redis) -> RedisCacher:
        return RedisCacher(client=client)

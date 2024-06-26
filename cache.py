from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.config.response_cache import (
    ResponseCacheConfig,
    default_cache_key_builder,
)
from litestar.stores.redis import RedisStore
from redis.asyncio import Redis

if TYPE_CHECKING:
    from litestar.connection import Request

app_slug = "litestar-mcve"

redis = Redis.from_url(
    url="redis://localhost:6379/0",
    encoding="utf-8",
    decode_responses=False,
    socket_connect_timeout=2,
    socket_keepalive=5,
    health_check_interval=5,
)
"""Async [`Redis`][redis.Redis] instance, configure via.

[CacheSettings][gateway.lib.config.CacheSettings].
"""


async def on_shutdown() -> None:
    """On Shutdown."""
    await redis.aclose()


def cache_key_builder(request: Request) -> str:
    """App name prefixed cache key builder.

    Parameters
    ----------
    request : Request
        Current request instance.

    Returns:
    -------
    str
        App slug prefixed cache key.
    """
    return f"{app_slug}:{default_cache_key_builder(request)}"


def redis_store_factory(name: str) -> RedisStore:
    return RedisStore(redis, namespace=f"{app_slug}:{name}")


config = ResponseCacheConfig(
    default_expiration=60,
    key_builder=cache_key_builder,
)
"""Cache configuration for application."""

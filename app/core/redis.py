from typing import AsyncGenerator
import redis.asyncio as aioredis
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Global redis client reference
redis_client: aioredis.Redis | None = None


async def init_redis() -> aioredis.Redis:
    """Initialize Redis connection pool."""
    global redis_client
    logger.info("Initializing Redis connection to %s", settings.redis_connection_url)
    redis_client = aioredis.from_url(
        settings.redis_connection_url,
        encoding="utf-8",
        decode_responses=True,
    )
    return redis_client


async def close_redis() -> None:
    """Close Redis connection."""
    global redis_client
    if redis_client:
        logger.info("Closing Redis connection...")
        await redis_client.aclose()
        redis_client = None


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """FastAPI dependency to retrieve the active Redis client."""
    global redis_client
    if redis_client is None:
        redis_client = await init_redis()
    yield redis_client

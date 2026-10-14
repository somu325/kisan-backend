from typing import Annotated
import redis.asyncio as aioredis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis import get_redis

# Annotated dependencies for cleaner endpoint definitions
SessionDep = Annotated[AsyncSession, Depends(get_db)]
RedisDep = Annotated[aioredis.Redis, Depends(get_redis)]

__all__ = ["SessionDep", "RedisDep", "get_db", "get_redis"]

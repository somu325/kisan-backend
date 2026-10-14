from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app import __version__
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    global_exception_handler,
)
from app.core.logging import get_logger, setup_logging
from app.core.redis import close_redis, init_redis

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifecycle manager."""
    logger.info("Starting up %s (v%s)...", settings.PROJECT_NAME, __version__)

    # 1. Initialize Redis connection pool
    try:
        await init_redis()
        logger.info("Redis connection established.")
    except Exception as exc:
        logger.warning("Redis could not be reached on startup: %s", exc)

    # 2. Check Database connectivity
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("PostgreSQL connection established.")
    except Exception as exc:
        logger.warning("PostgreSQL could not be reached on startup: %s", exc)

    yield

    # Shutdown
    logger.info("Shutting down %s...", settings.PROJECT_NAME)
    await close_redis()
    await engine.dispose()
    logger.info("Resources cleaned up successfully.")


def create_application() -> FastAPI:
    """FastAPI Application Factory."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=__version__,
        description="Production-grade FastAPI backend for Kisan with Redis, PostgreSQL, External APIs, and Scraping support.",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Middleware: CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS if isinstance(settings.ALLOWED_ORIGINS, list) else [settings.ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    # Routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": __version__,
            "status": "running",
            "docs": "/docs",
            "api": settings.API_V1_STR,
        }

    return app


app = create_application()

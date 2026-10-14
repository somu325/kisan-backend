from fastapi import APIRouter, status
from sqlalchemy import text
from app import __version__
from app.api.deps import RedisDep, SessionDep
from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.common import APIResponse, HealthStatusResponse

logger = get_logger(__name__)
router = APIRouter()


@router.get(
    "/health",
    response_model=APIResponse[HealthStatusResponse],
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check connectivity to PostgreSQL database and Redis cache.",
)
async def check_health(db: SessionDep, redis: RedisDep) -> APIResponse[HealthStatusResponse]:
    # Check Database Connectivity
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error("PostgreSQL health check failed: %s", str(e))
        db_status = f"unhealthy: {str(e)}"

    # Check Redis Connectivity
    redis_status = "healthy"
    try:
        pong = await redis.ping()
        if not pong:
            redis_status = "unhealthy: no response"
    except Exception as e:
        logger.error("Redis health check failed: %s", str(e))
        redis_status = f"unhealthy: {str(e)}"

    overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded"

    return APIResponse(
        success=overall_status == "healthy",
        message=f"System is {overall_status}",
        data=HealthStatusResponse(
            status=overall_status,
            environment=settings.ENVIRONMENT,
            database=db_status,
            redis=redis_status,
            version=__version__,
        ),
    )

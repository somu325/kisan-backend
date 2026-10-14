from fastapi import APIRouter
from app.schemas.common import APIResponse

router = APIRouter()


@router.get(
    "/status",
    response_model=APIResponse[dict],
    summary="Scraper Status (Placeholder)",
)
async def scraper_status() -> APIResponse[dict]:
    """Placeholder endpoint for web scraper status and triggers."""
    return APIResponse(
        success=True,
        message="Web scraping service endpoint ready for implementation",
        data={"active_jobs": 0},
    )

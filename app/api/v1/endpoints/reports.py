from fastapi import APIRouter
from app.schemas.common import APIResponse

router = APIRouter()


@router.get(
    "/",
    response_model=APIResponse[dict],
    summary="List Reports (Placeholder)",
)
async def list_reports() -> APIResponse[dict]:
    """Placeholder endpoint for report generation and retrieval."""
    return APIResponse(
        success=True,
        message="Reports endpoint ready for implementation",
        data={"items": []},
    )

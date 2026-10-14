from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class APIResponse(BaseSchema, Generic[T]):
    """Standardized API response structure for frontend communication."""
    success: bool = True
    message: Optional[str] = "Operation successful"
    data: Optional[T] = None


class PaginatedResponse(BaseSchema, Generic[T]):
    """Standardized paginated list response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class HealthStatusResponse(BaseSchema):
    """Health check response schema."""
    status: str
    environment: str
    database: str
    redis: str
    version: str

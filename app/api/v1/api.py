from fastapi import APIRouter
from app.api.v1.endpoints import health, reports, scrapers

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(scrapers.router, prefix="/scrapers", tags=["Scrapers"])

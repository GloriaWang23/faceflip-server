"""Health check endpoints"""

from fastapi import APIRouter

from app.core.config import settings
from app.core.response import success


router = APIRouter()


@router.get("")
async def health_check():
    """Comprehensive health check"""
    return success(
        data={
            "status": "healthy",
            "app": settings.app_name,
            "version": settings.app_version,
            "environment": "development" if settings.debug else "production"
        }
    )

@router.get("/health/check")
async def health_check_db():
    """Health check database"""
    return success(data={"message": "Database is healthy"})

@router.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return success(data={"message": "pong"})


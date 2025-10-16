"""API router aggregation"""

from fastapi import APIRouter

from app.api.endpoints import auth, users, health, order, faceflip

# Create main API router
api_router = APIRouter()


# Include all endpoint routers
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    order.router,
    prefix="/orders",
    tags=["orders"]
)

api_router.include_router(
    faceflip.router,
    prefix="/faceflip",
    tags=["faceflip"]
)


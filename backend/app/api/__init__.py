"""API router configuration."""

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.project import router as project_router
from app.api.v1.routers.folder import router as folder_router
from app.api.v1.routers.snippet import router as snippet_router


def get_api_router() -> APIRouter:
    """
    Create and configure main API router.

    Returns:
        Configured APIRouter with all endpoints
    """
    router = APIRouter(route_class=DishkaRoute)

    # Include authentication routes
    router.include_router(auth_router)

    # Include project management routes
    router.include_router(project_router)
    router.include_router(folder_router)
    router.include_router(snippet_router)

    return router

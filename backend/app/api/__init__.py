"""API router configuration."""
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.api.v1.routers.auth import router as auth_router


def get_api_router() -> APIRouter:
    """
    Create and configure main API router.

    Returns:
        Configured APIRouter with all endpoints
    """
    router = APIRouter(route_class=DishkaRoute)

    # Include authentication routes
    router.include_router(auth_router)

    # TODO: Include other routers (projects, snippets, folders, etc.)
    # router.include_router(projects.router)
    # router.include_router(snippets.router)
    # router.include_router(folders.router)

    return router

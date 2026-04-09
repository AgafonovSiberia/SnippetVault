import logging
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Query, status

from app.api.schemas.project import ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse
from app.api.schemas.common import PageResponse
from app.application.project.project_service import ProjectService
from app.application.project.project_dto import ProjectCreateDTO, ProjectUpdateDTO
from app.application.common.pagination import PageParams
from app.di import AuthenticatedUser

logger = logging.getLogger(__name__)

router = APIRouter(route_class=DishkaRoute, prefix="/projects", tags=["Projects"])


@router.get("/", response_model=PageResponse[ProjectResponse])
async def get_projects(
    current_user: FromDishka[AuthenticatedUser],
    project_service: FromDishka[ProjectService],
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> PageResponse[ProjectResponse]:
    page = await project_service.get_user_projects(current_user.id, PageParams(limit, offset))
    return PageResponse(
        items=[ProjectResponse.model_validate(p) for p in page.items],
        total=page.total,
        limit=page.limit,
        offset=page.offset,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    current_user: FromDishka[AuthenticatedUser],
    project_service: FromDishka[ProjectService],
) -> ProjectResponse:
    project = await project_service.get_project(project_id, current_user.id)
    return ProjectResponse.model_validate(project)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreateRequest,
    current_user: FromDishka[AuthenticatedUser],
    project_service: FromDishka[ProjectService],
) -> ProjectResponse:
    project = await project_service.create_project(
        current_user.id, ProjectCreateDTO.model_validate(data)
    )
    return ProjectResponse.model_validate(project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    data: ProjectUpdateRequest,
    current_user: FromDishka[AuthenticatedUser],
    project_service: FromDishka[ProjectService],
) -> ProjectResponse:
    project = await project_service.update_project(
        project_id, current_user.id, ProjectUpdateDTO.model_validate(data)
    )
    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    current_user: FromDishka[AuthenticatedUser],
    project_service: FromDishka[ProjectService],
) -> None:
    await project_service.delete_project(project_id, current_user.id)

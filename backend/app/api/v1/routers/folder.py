import logging
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Query, status

from app.api.schemas.folder import FolderCreateRequest, FolderUpdateRequest, FolderResponse
from app.api.schemas.common import PageResponse
from app.application.project.folder_service import FolderService
from app.application.project.folder_dto import FolderCreateDTO, FolderUpdateDTO
from app.application.common.pagination import PageParams
from app.di import AuthenticatedUser

logger = logging.getLogger(__name__)

router = APIRouter(route_class=DishkaRoute, prefix="/folders", tags=["Folders"])


@router.get("/", response_model=PageResponse[FolderResponse])
async def get_folders(
    current_user: FromDishka[AuthenticatedUser],
    folder_service: FromDishka[FolderService],
    project_id: UUID | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> PageResponse[FolderResponse]:
    page = await folder_service.get_folders(
        current_user.id, project_id, PageParams(limit, offset)
    )
    return PageResponse(
        items=[FolderResponse.model_validate(f) for f in page.items],
        total=page.total,
        limit=page.limit,
        offset=page.offset,
    )


@router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder(
    folder_id: UUID,
    current_user: FromDishka[AuthenticatedUser],
    folder_service: FromDishka[FolderService],
) -> FolderResponse:
    folder = await folder_service.get_folder(folder_id, current_user.id)
    return FolderResponse.model_validate(folder)


@router.post("/", response_model=FolderResponse, status_code=status.HTTP_201_CREATED)
async def create_folder(
    data: FolderCreateRequest,
    current_user: FromDishka[AuthenticatedUser],
    folder_service: FromDishka[FolderService],
) -> FolderResponse:
    folder = await folder_service.create_folder(
        current_user.id, FolderCreateDTO.model_validate(data)
    )
    return FolderResponse.model_validate(folder)


@router.put("/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: UUID,
    data: FolderUpdateRequest,
    current_user: FromDishka[AuthenticatedUser],
    folder_service: FromDishka[FolderService],
) -> FolderResponse:
    folder = await folder_service.update_folder(
        folder_id, current_user.id, FolderUpdateDTO.model_validate(data)
    )
    return FolderResponse.model_validate(folder)


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(
    folder_id: UUID,
    current_user: FromDishka[AuthenticatedUser],
    folder_service: FromDishka[FolderService],
) -> None:
    await folder_service.delete_folder(folder_id, current_user.id)

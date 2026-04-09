import logging
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Query, status

from app.api.schemas.snippet import (
    SnippetCreateRequest, SnippetUpdateRequest, SnippetResponse, SearchResponse
)
from app.api.schemas.common import PageResponse
from app.application.project.snippet_service import SnippetService
from app.application.project.snippet_dto import SnippetCreateDTO, SnippetUpdateDTO
from app.application.common.pagination import PageParams
from app.di import AuthenticatedUser

logger = logging.getLogger(__name__)

router = APIRouter(route_class=DishkaRoute, prefix="/snippets", tags=["Snippets"])


@router.get("/", response_model=PageResponse[SnippetResponse])
async def get_snippets(
    current_user: FromDishka[AuthenticatedUser],
    snippet_service: FromDishka[SnippetService],
    project_id: UUID | None = Query(None),
    folder_id: UUID | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> PageResponse[SnippetResponse]:
    page = await snippet_service.get_snippets(
        current_user.id, project_id, folder_id, PageParams(limit, offset)
    )
    return PageResponse(
        items=[SnippetResponse.model_validate(s) for s in page.items],
        total=page.total,
        limit=page.limit,
        offset=page.offset,
    )


@router.get("/search", response_model=SearchResponse)
async def search_snippets(
    current_user: FromDishka[AuthenticatedUser],
    snippet_service: FromDishka[SnippetService],
    q: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> SearchResponse:
    page = await snippet_service.search_snippets(current_user.id, q, PageParams(limit, offset))
    return SearchResponse(
        snippets=[SnippetResponse.model_validate(s) for s in page.items],
        total=page.total,
        limit=page.limit,
        offset=page.offset,
    )


@router.get("/{snippet_id}", response_model=SnippetResponse)
async def get_snippet(
    snippet_id: UUID,
    current_user: FromDishka[AuthenticatedUser],
    snippet_service: FromDishka[SnippetService],
) -> SnippetResponse:
    snippet = await snippet_service.get_snippet(snippet_id, current_user.id)
    return SnippetResponse.model_validate(snippet)


@router.post("/", response_model=SnippetResponse, status_code=status.HTTP_201_CREATED)
async def create_snippet(
    data: SnippetCreateRequest,
    current_user: FromDishka[AuthenticatedUser],
    snippet_service: FromDishka[SnippetService],
) -> SnippetResponse:
    snippet = await snippet_service.create_snippet(
        current_user.id, SnippetCreateDTO.model_validate(data)
    )
    return SnippetResponse.model_validate(snippet)


@router.put("/{snippet_id}", response_model=SnippetResponse)
async def update_snippet(
    snippet_id: UUID,
    data: SnippetUpdateRequest,
    current_user: FromDishka[AuthenticatedUser],
    snippet_service: FromDishka[SnippetService],
) -> SnippetResponse:
    snippet = await snippet_service.update_snippet(
        snippet_id, current_user.id, SnippetUpdateDTO.model_validate(data)
    )
    return SnippetResponse.model_validate(snippet)


@router.delete("/{snippet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_snippet(
    snippet_id: UUID,
    current_user: FromDishka[AuthenticatedUser],
    snippet_service: FromDishka[SnippetService],
) -> None:
    await snippet_service.delete_snippet(snippet_id, current_user.id)


@router.post("/{snippet_id}/favorite", response_model=SnippetResponse)
async def toggle_favorite(
    snippet_id: UUID,
    current_user: FromDishka[AuthenticatedUser],
    snippet_service: FromDishka[SnippetService],
) -> SnippetResponse:
    snippet = await snippet_service.toggle_favorite(snippet_id, current_user.id)
    return SnippetResponse.model_validate(snippet)

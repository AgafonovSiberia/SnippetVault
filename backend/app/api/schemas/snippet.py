from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class SnippetCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(...)
    language: str = Field(..., max_length=50)
    project_id: UUID
    folder_id: UUID | None = None
    description: str | None = None
    tags: list[str] | None = None


class SnippetUpdateRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = None
    language: str | None = Field(None, max_length=50)
    folder_id: UUID | None = None
    description: str | None = None
    tags: list[str] | None = None
    is_favorite: bool | None = None


class SnippetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    folder_id: UUID | None
    title: str
    content: str
    language: str
    description: str | None = None
    is_favorite: bool
    created_at: datetime
    updated_at: datetime
    tags: list[str] = []


class SearchResponse(BaseModel):
    snippets: list[SnippetResponse]
    total: int
    limit: int
    offset: int

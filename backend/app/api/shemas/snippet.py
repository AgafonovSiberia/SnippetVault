"""
API Schemas for Snippets
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class SnippetCreateRequest(BaseModel):
    """Запрос на создание сниппета"""

    title: str = Field(..., min_length=1, max_length=200, description="Snippet title")
    content: str = Field(..., description="Snippet content")
    language: str = Field(..., max_length=50, description="Programming language")
    project_id: UUID = Field(..., description="Project ID")
    folder_id: UUID | None = Field(None, description="Folder ID")
    description: str | None = Field(None, description="Snippet description")
    tags: list[str] | None = Field(None, description="Tags")


class SnippetUpdateRequest(BaseModel):
    """Запрос на обновление сниппета"""

    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = None
    language: str | None = Field(None, max_length=50)
    folder_id: UUID | None = None
    description: str | None = None
    tags: list[str] | None = None
    is_favorite: bool | None = None


class SnippetResponse(BaseModel):
    """Ответ с данными сниппета"""

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


class SearchResultResponse(BaseModel):
    """Ответ с результатами поиска"""

    snippets: list[SnippetResponse]
    total: int

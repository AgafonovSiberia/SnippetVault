"""
API Schemas for Projects
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class ProjectCreateRequest(BaseModel):
    """Запрос на создание проекта"""

    name: str = Field(..., min_length=1, max_length=120, description="Project name")
    description: str | None = Field(None, description="Project description")
    color: str | None = Field(None, description="Project color")


class ProjectUpdateRequest(BaseModel):
    """Запрос на обновление проекта"""

    name: str | None = Field(None, min_length=1, max_length=120)
    description: str | None = None
    color: str | None = None


class ProjectResponse(BaseModel):
    """Ответ с данными проекта"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    snippets_count: int = 0
    folders_count: int = 0

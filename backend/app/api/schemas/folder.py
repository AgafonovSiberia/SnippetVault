"""
API Schemas for Folders
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class FolderCreateRequest(BaseModel):
    """Запрос на создание папки"""

    name: str = Field(..., min_length=1, max_length=120, description="Folder name")
    project_id: UUID = Field(..., description="Parent project ID")
    parent_folder_id: UUID | None = Field(None, description="Parent folder ID")
    description: str | None = Field(None, description="Folder description")
    color: str | None = Field(None, description="Folder color")
    icon: str | None = Field(None, description="Folder icon")


class FolderUpdateRequest(BaseModel):
    """Запрос на обновление папки"""

    name: str | None = Field(None, min_length=1, max_length=120)
    description: str | None = None
    color: str | None = None
    icon: str | None = None


class FolderResponse(BaseModel):
    """Ответ с данными папки"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    parent_folder_id: UUID | None = None
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    snippets_count: int = 0

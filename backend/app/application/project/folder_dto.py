from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class FolderCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    name: str = Field(..., min_length=1, max_length=120)
    project_id: UUID
    parent_folder_id: UUID | None = None
    description: str | None = None


class FolderUpdateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    name: str | None = Field(None, min_length=1, max_length=120)
    description: str | None = None


class FolderDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: UUID
    project_id: UUID
    parent_folder_id: UUID | None = None
    name: str = Field(validation_alias="title")
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    snippets_count: int = 0

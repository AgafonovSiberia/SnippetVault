from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class ProjectCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    name: str = Field(..., min_length=1, max_length=120)
    description: str | None = None


class ProjectUpdateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    name: str | None = Field(None, min_length=1, max_length=120)
    description: str | None = None


class ProjectDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: UUID
    name: str = Field(validation_alias="title")
    description: str | None
    created_at: datetime
    updated_at: datetime
    snippets_count: int = 0
    folders_count: int = 0

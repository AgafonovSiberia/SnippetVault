from pydantic import BaseModel, Field, ConfigDict, field_validator
from uuid import UUID
from datetime import datetime


class SnippetCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    title: str = Field(..., min_length=1, max_length=200)
    content: str
    language: str = Field(..., max_length=50)
    project_id: UUID
    folder_id: UUID | None = None
    description: str | None = None
    tags: list[str] = Field(default_factory=list)


class SnippetUpdateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = None
    language: str | None = Field(None, max_length=50)
    folder_id: UUID | None = None
    description: str | None = None
    tags: list[str] | None = None
    is_favorite: bool | None = None


class SnippetDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: UUID
    project_id: UUID
    folder_id: UUID | None
    title: str
    content: str
    language: str
    description: str | None = None
    is_favorite: bool = Field(validation_alias="pinned", default=False)
    created_at: datetime
    updated_at: datetime
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags", mode="before")
    @classmethod
    def extract_tag_names(cls, v):
        if not v:
            return []
        if v and hasattr(v[0], "normalized_name"):
            return [tag.normalized_name for tag in v]
        return list(v)

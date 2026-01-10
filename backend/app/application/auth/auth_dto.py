from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserDTO(BaseModel):
    id: UUID
    display_name: str | None = None
    avatar_url: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuthTokensDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthResponseDTO(BaseModel):
    user: UserDTO
    tokens: AuthTokensDTO

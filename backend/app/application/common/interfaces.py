from typing import Protocol
from uuid import UUID

from app.application.common.sentinel import UNSET, _UnsetType


class IProjectRepo(Protocol):
    async def get_user_projects_with_stats(
        self, user_id: UUID, limit: int, offset: int
    ) -> tuple[list, int]: ...

    async def get_project_by_id(self, project_id: UUID, user_id: UUID): ...

    async def get_project_stats(self, project_id: UUID) -> tuple[int, int]: ...

    async def create_project(
        self, user_id: UUID, title: str, description: str | None = None
    ): ...

    async def update_project(
        self,
        project,
        title: str | _UnsetType = UNSET,
        description: str | None | _UnsetType = UNSET,
    ): ...

    async def delete_project(self, project) -> None: ...

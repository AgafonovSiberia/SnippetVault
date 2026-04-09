"""
Repository for Folders
"""

import logging
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import Folder, Snippet, Project

logger = logging.getLogger(__name__)


class FolderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_project_folders(
        self, project_id: UUID, limit: int = 50, offset: int = 0
    ) -> tuple[list[Folder], int]:
        total = (await self.session.execute(
            select(func.count(Folder.id)).where(Folder.project_id == project_id)
        )).scalar() or 0

        rows = await self.session.execute(
            select(Folder)
            .where(Folder.project_id == project_id)
            .order_by(Folder.sort_order, Folder.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(rows.scalars().all()), total

    async def get_user_folders(
        self, user_id: UUID, limit: int = 50, offset: int = 0
    ) -> tuple[list[Folder], int]:
        total = (await self.session.execute(
            select(func.count(Folder.id))
            .join(Project, Project.id == Folder.project_id)
            .where(Project.user_id == user_id)
        )).scalar() or 0

        rows = await self.session.execute(
            select(Folder)
            .join(Project, Project.id == Folder.project_id)
            .where(Project.user_id == user_id)
            .order_by(Folder.sort_order, Folder.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(rows.scalars().all()), total

    async def get_folder_by_id(self, folder_id: UUID) -> Folder | None:
        result = await self.session.execute(select(Folder).where(Folder.id == folder_id))
        return result.scalar_one_or_none()

    async def create_folder(self, project_id: UUID, title: str) -> Folder:
        folder = Folder(project_id=project_id, title=title)
        self.session.add(folder)
        await self.session.flush()
        await self.session.refresh(folder)
        return folder

    async def update_folder(self, folder: Folder, title: str | None = None) -> Folder:
        if title is not None:
            folder.title = title
        await self.session.flush()
        await self.session.refresh(folder)
        return folder

    async def delete_folder(self, folder: Folder) -> None:
        await self.session.delete(folder)
        await self.session.flush()

    async def get_folder_snippets_count(self, folder_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(Snippet).where(Snippet.folder_id == folder_id)
        )
        return result.scalar() or 0

    async def get_snippets_count_by_folder_ids(
        self, folder_ids: list[UUID]
    ) -> dict[UUID, int]:
        if not folder_ids:
            return {}
        result = await self.session.execute(
            select(Snippet.folder_id, func.count().label("cnt"))
            .where(Snippet.folder_id.in_(folder_ids))
            .group_by(Snippet.folder_id)
        )
        return {row.folder_id: row.cnt for row in result.all()}

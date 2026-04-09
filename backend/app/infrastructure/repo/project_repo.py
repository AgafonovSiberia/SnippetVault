"""
Repository for Projects
"""

import logging
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import Project, Folder, Snippet
from app.application.common.sentinel import UNSET, _UnsetType

logger = logging.getLogger(__name__)


class ProjectRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_projects_with_stats(
        self, user_id: UUID, limit: int = 50, offset: int = 0
    ) -> tuple[list[tuple[Project, int, int]], int]:
        """Проекты со статистикой + общее количество — двумя запросами."""
        total_result = await self.session.execute(
            select(func.count(Project.id)).where(Project.user_id == user_id)
        )
        total = total_result.scalar() or 0

        rows_result = await self.session.execute(
            select(
                Project,
                func.count(Folder.id.distinct()).label("folders_count"),
                func.count(Snippet.id.distinct()).label("snippets_count"),
            )
            .outerjoin(Folder, Folder.project_id == Project.id)
            .outerjoin(Snippet, Snippet.project_id == Project.id)
            .where(Project.user_id == user_id)
            .group_by(Project.id)
            .order_by(Project.sort_order, Project.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        rows = [(r.Project, r.folders_count, r.snippets_count) for r in rows_result.all()]
        return rows, total

    async def get_project_by_id(self, project_id: UUID, user_id: UUID) -> Project | None:
        result = await self.session.execute(
            select(Project).where(Project.id == project_id, Project.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_project(
        self, user_id: UUID, title: str, description: str | None = None
    ) -> Project:
        project = Project(user_id=user_id, title=title, description=description)
        self.session.add(project)
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def update_project(
        self,
        project: Project,
        title: str | _UnsetType = UNSET,
        description: str | None | _UnsetType = UNSET,
    ) -> Project:
        if not isinstance(title, _UnsetType):
            project.title = title
        if not isinstance(description, _UnsetType):
            project.description = description
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def delete_project(self, project: Project) -> None:
        await self.session.delete(project)
        await self.session.flush()

    async def get_project_stats(self, project_id: UUID) -> tuple[int, int]:
        result = await self.session.execute(
            select(
                func.count(Folder.id.distinct()).label("folders_count"),
                func.count(Snippet.id.distinct()).label("snippets_count"),
            )
            .select_from(Project)
            .outerjoin(Folder, Folder.project_id == Project.id)
            .outerjoin(Snippet, Snippet.project_id == Project.id)
            .where(Project.id == project_id)
            .group_by(Project.id)
        )
        row = result.one_or_none()
        if row is None:
            return 0, 0
        return row.folders_count, row.snippets_count

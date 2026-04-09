"""
Repository for Snippets and Tags
"""

import logging
import uuid as uuid_module
from uuid import UUID
from sqlalchemy import select, func, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import Project, Snippet, Tag, SnippetTag
from app.application.common.sentinel import UNSET, _UnsetType

logger = logging.getLogger(__name__)


class SnippetRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ==================== Snippets ====================

    async def get_project_snippets(
        self,
        project_id: UUID,
        folder_id: UUID | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Snippet], int]:
        base = select(Snippet).where(Snippet.project_id == project_id)
        if folder_id is not None:
            base = base.where(Snippet.folder_id == folder_id)

        total = (await self.session.execute(
            select(func.count()).select_from(base.subquery())
        )).scalar() or 0

        rows = await self.session.execute(
            base.options(selectinload(Snippet.tags))
            .order_by(Snippet.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(rows.scalars().all()), total

    async def get_user_snippets(
        self, user_id: UUID, limit: int = 50, offset: int = 0
    ) -> tuple[list[Snippet], int]:
        base = select(Snippet).join(Project).where(Project.user_id == user_id)

        total = (await self.session.execute(
            select(func.count()).select_from(base.subquery())
        )).scalar() or 0

        rows = await self.session.execute(
            base.options(selectinload(Snippet.tags))
            .order_by(Snippet.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(rows.scalars().all()), total

    async def get_snippet_by_id(self, snippet_id: UUID) -> Snippet | None:
        result = await self.session.execute(
            select(Snippet).options(selectinload(Snippet.tags)).where(Snippet.id == snippet_id)
        )
        return result.scalar_one_or_none()

    async def create_snippet(
        self,
        project_id: UUID,
        title: str,
        content: str,
        language: str,
        folder_id: UUID | None = None,
    ) -> Snippet:
        snippet = Snippet(
            project_id=project_id,
            folder_id=folder_id,
            title=title,
            content=content,
            language=language,
        )
        self.session.add(snippet)
        await self.session.flush()
        await self.session.refresh(snippet, ["tags"])
        return snippet

    async def update_snippet(
        self,
        snippet: Snippet,
        title: str | _UnsetType = UNSET,
        content: str | _UnsetType = UNSET,
        language: str | _UnsetType = UNSET,
        folder_id: UUID | None | _UnsetType = UNSET,
        pinned: bool | _UnsetType = UNSET,
    ) -> Snippet:
        if not isinstance(title, _UnsetType):
            snippet.title = title
        if not isinstance(content, _UnsetType):
            snippet.content = content
        if not isinstance(language, _UnsetType):
            snippet.language = language
        if not isinstance(folder_id, _UnsetType):
            snippet.folder_id = folder_id
        if not isinstance(pinned, _UnsetType):
            snippet.pinned = pinned
        await self.session.flush()
        await self.session.refresh(snippet, ["tags"])
        return snippet

    async def delete_snippet(self, snippet: Snippet) -> None:
        await self.session.delete(snippet)
        await self.session.flush()

    async def toggle_snippet_favorite(self, snippet: Snippet) -> Snippet:
        snippet.pinned = not snippet.pinned
        await self.session.flush()
        await self.session.refresh(snippet, ["tags"])
        return snippet

    # ==================== Tags ====================

    async def get_or_create_tag(self, user_id: UUID, tag_name: str) -> Tag:
        normalized_name = tag_name.lower().strip()
        await self.session.execute(
            pg_insert(Tag)
            .values(id=uuid_module.uuid4(), user_id=user_id, normalized_name=normalized_name)
            .on_conflict_do_nothing(constraint="uq_user_tag")
        )
        result = await self.session.execute(
            select(Tag).where(Tag.user_id == user_id, Tag.normalized_name == normalized_name)
        )
        return result.scalar_one()

    async def set_snippet_tags(
        self, snippet: Snippet, user_id: UUID, tag_names: list[str]
    ) -> None:
        await self.session.execute(
            delete(SnippetTag).where(SnippetTag.snippet_id == snippet.id)
        )
        for tag_name in tag_names:
            tag = await self.get_or_create_tag(user_id, tag_name)
            self.session.add(SnippetTag(snippet_id=snippet.id, tag_id=tag.id))
        await self.session.flush()

    # ==================== Search ====================

    async def search_snippets(
        self, user_id: UUID, query: str, limit: int = 50, offset: int = 0
    ) -> tuple[list[Snippet], int]:
        search_pattern = f"%{query}%"
        match_condition = (
            Snippet.title.ilike(search_pattern)
            | Snippet.content.ilike(search_pattern)
            | Tag.normalized_name.ilike(search_pattern)
        )
        base = (
            select(Snippet)
            .join(Project, Project.id == Snippet.project_id)
            .outerjoin(SnippetTag, SnippetTag.snippet_id == Snippet.id)
            .outerjoin(Tag, Tag.id == SnippetTag.tag_id)
            .where(Project.user_id == user_id, match_condition)
            .distinct()
        )

        total = (await self.session.execute(
            select(func.count()).select_from(base.subquery())
        )).scalar() or 0

        rows = await self.session.execute(
            base.options(selectinload(Snippet.tags))
            .order_by(Snippet.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(rows.scalars().all()), total

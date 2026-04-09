import logging
from uuid import UUID

from app.application.project.snippet_dto import SnippetDTO, SnippetCreateDTO, SnippetUpdateDTO
from app.application.common.exceptions import ResourceNotFoundError, PermissionDeniedError
from app.application.common.sentinel import UNSET
from app.application.common.pagination import Page, PageParams
from app.infrastructure.repo.snippet_repo import SnippetRepo
from app.infrastructure.repo.project_repo import ProjectRepo
from app.infrastructure.repo.folder_repo import FolderRepo

logger = logging.getLogger(__name__)


class SnippetService:
    def __init__(
        self,
        project_repo: ProjectRepo,
        folder_repo: FolderRepo,
        snippet_repo: SnippetRepo,
    ):
        self.project_repo = project_repo
        self.folder_repo = folder_repo
        self.snippet_repo = snippet_repo

    async def get_snippets(
        self,
        user_id: UUID,
        project_id: UUID | None,
        folder_id: UUID | None,
        page: PageParams = PageParams(),
    ) -> Page[SnippetDTO]:
        if project_id is not None:
            project = await self.project_repo.get_project_by_id(project_id, user_id)
            if not project:
                raise ResourceNotFoundError(f"Project {project_id} not found")
            snippets, total = await self.snippet_repo.get_project_snippets(
                project_id, folder_id, limit=page.limit, offset=page.offset
            )
        else:
            snippets, total = await self.snippet_repo.get_user_snippets(
                user_id, limit=page.limit, offset=page.offset
            )
        items = [SnippetDTO.model_validate(s) for s in snippets]
        return Page(items=items, total=total, limit=page.limit, offset=page.offset)

    async def get_snippet(self, snippet_id: UUID, user_id: UUID) -> SnippetDTO:
        snippet = await self.snippet_repo.get_snippet_by_id(snippet_id)
        if not snippet:
            raise ResourceNotFoundError(f"Snippet {snippet_id} not found")
        project = await self.project_repo.get_project_by_id(snippet.project_id, user_id)
        if not project:
            raise PermissionDeniedError("Access denied")
        return SnippetDTO.model_validate(snippet)

    async def create_snippet(self, user_id: UUID, data: SnippetCreateDTO) -> SnippetDTO:
        project = await self.project_repo.get_project_by_id(data.project_id, user_id)
        if not project:
            raise ResourceNotFoundError(f"Project {data.project_id} not found")
        snippet = await self.snippet_repo.create_snippet(
            project_id=data.project_id,
            title=data.title,
            content=data.content,
            language=data.language,
            folder_id=data.folder_id,
        )
        if data.tags:
            await self.snippet_repo.set_snippet_tags(snippet, user_id, data.tags)
            snippet = await self.snippet_repo.get_snippet_by_id(snippet.id)
        logger.info(f"Snippet {snippet.id} created in project {data.project_id}")
        return SnippetDTO.model_validate(snippet)

    async def update_snippet(
        self, snippet_id: UUID, user_id: UUID, data: SnippetUpdateDTO
    ) -> SnippetDTO:
        snippet = await self.snippet_repo.get_snippet_by_id(snippet_id)
        if not snippet:
            raise ResourceNotFoundError(f"Snippet {snippet_id} not found")
        project = await self.project_repo.get_project_by_id(snippet.project_id, user_id)
        if not project:
            raise PermissionDeniedError("Access denied")

        fields = data.model_fields_set
        snippet = await self.snippet_repo.update_snippet(
            snippet,
            title=data.title if "title" in fields else UNSET,
            content=data.content if "content" in fields else UNSET,
            language=data.language if "language" in fields else UNSET,
            folder_id=data.folder_id if "folder_id" in fields else UNSET,
            pinned=data.is_favorite if "is_favorite" in fields else UNSET,
        )
        if "tags" in fields and data.tags is not None:
            await self.snippet_repo.set_snippet_tags(snippet, user_id, data.tags)
            snippet = await self.snippet_repo.get_snippet_by_id(snippet.id)

        logger.info(f"Snippet {snippet_id} updated")
        return SnippetDTO.model_validate(snippet)

    async def delete_snippet(self, snippet_id: UUID, user_id: UUID) -> None:
        snippet = await self.snippet_repo.get_snippet_by_id(snippet_id)
        if not snippet:
            raise ResourceNotFoundError(f"Snippet {snippet_id} not found")
        project = await self.project_repo.get_project_by_id(snippet.project_id, user_id)
        if not project:
            raise PermissionDeniedError("Access denied")
        await self.snippet_repo.delete_snippet(snippet)
        logger.info(f"Snippet {snippet_id} deleted")

    async def toggle_favorite(self, snippet_id: UUID, user_id: UUID) -> SnippetDTO:
        snippet = await self.snippet_repo.get_snippet_by_id(snippet_id)
        if not snippet:
            raise ResourceNotFoundError(f"Snippet {snippet_id} not found")
        project = await self.project_repo.get_project_by_id(snippet.project_id, user_id)
        if not project:
            raise PermissionDeniedError("Access denied")
        snippet = await self.snippet_repo.toggle_snippet_favorite(snippet)
        return SnippetDTO.model_validate(snippet)

    async def search_snippets(
        self, user_id: UUID, query: str, page: PageParams = PageParams()
    ) -> Page[SnippetDTO]:
        snippets, total = await self.snippet_repo.search_snippets(
            user_id, query, limit=page.limit, offset=page.offset
        )
        items = [SnippetDTO.model_validate(s) for s in snippets]
        return Page(items=items, total=total, limit=page.limit, offset=page.offset)

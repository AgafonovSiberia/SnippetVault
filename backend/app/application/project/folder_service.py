import logging
from uuid import UUID

from app.application.project.folder_dto import FolderDTO, FolderCreateDTO, FolderUpdateDTO
from app.application.common.exceptions import ResourceNotFoundError, PermissionDeniedError
from app.application.common.pagination import Page, PageParams
from app.infrastructure.repo.folder_repo import FolderRepo
from app.infrastructure.repo.project_repo import ProjectRepo

logger = logging.getLogger(__name__)


class FolderService:
    def __init__(self, project_repo: ProjectRepo, folder_repo: FolderRepo):
        self.project_repo = project_repo
        self.folder_repo = folder_repo

    async def get_folders(
        self, user_id: UUID, project_id: UUID | None, page: PageParams = PageParams()
    ) -> Page[FolderDTO]:
        if project_id is not None:
            project = await self.project_repo.get_project_by_id(project_id, user_id)
            if not project:
                raise ResourceNotFoundError(f"Project {project_id} not found")
            folders, total = await self.folder_repo.get_project_folders(
                project_id, limit=page.limit, offset=page.offset
            )
        else:
            folders, total = await self.folder_repo.get_user_folders(
                user_id, limit=page.limit, offset=page.offset
            )

        folder_ids = [f.id for f in folders]
        counts = await self.folder_repo.get_snippets_count_by_folder_ids(folder_ids)

        items = []
        for folder in folders:
            dto = FolderDTO.model_validate(folder)
            dto.snippets_count = counts.get(folder.id, 0)
            items.append(dto)

        return Page(items=items, total=total, limit=page.limit, offset=page.offset)

    async def get_folder(self, folder_id: UUID, user_id: UUID) -> FolderDTO:
        folder = await self.folder_repo.get_folder_by_id(folder_id)
        if not folder:
            raise ResourceNotFoundError(f"Folder {folder_id} not found")
        project = await self.project_repo.get_project_by_id(folder.project_id, user_id)
        if not project:
            raise PermissionDeniedError("Access denied")
        snippets_count = await self.folder_repo.get_folder_snippets_count(folder_id)
        dto = FolderDTO.model_validate(folder)
        dto.snippets_count = snippets_count
        return dto

    async def create_folder(self, user_id: UUID, data: FolderCreateDTO) -> FolderDTO:
        project = await self.project_repo.get_project_by_id(data.project_id, user_id)
        if not project:
            raise ResourceNotFoundError(f"Project {data.project_id} not found")
        folder = await self.folder_repo.create_folder(
            project_id=data.project_id, title=data.name
        )
        logger.info(f"Folder {folder.id} created in project {data.project_id}")
        return FolderDTO.model_validate(folder)

    async def update_folder(
        self, folder_id: UUID, user_id: UUID, data: FolderUpdateDTO
    ) -> FolderDTO:
        folder = await self.folder_repo.get_folder_by_id(folder_id)
        if not folder:
            raise ResourceNotFoundError(f"Folder {folder_id} not found")
        project = await self.project_repo.get_project_by_id(folder.project_id, user_id)
        if not project:
            raise PermissionDeniedError("Access denied")
        folder = await self.folder_repo.update_folder(
            folder,
            title=data.name if data.name is not None else None,
        )
        logger.info(f"Folder {folder_id} updated")
        return FolderDTO.model_validate(folder)

    async def delete_folder(self, folder_id: UUID, user_id: UUID) -> None:
        folder = await self.folder_repo.get_folder_by_id(folder_id)
        if not folder:
            raise ResourceNotFoundError(f"Folder {folder_id} not found")
        project = await self.project_repo.get_project_by_id(folder.project_id, user_id)
        if not project:
            raise PermissionDeniedError("Access denied")
        await self.folder_repo.delete_folder(folder)
        logger.info(f"Folder {folder_id} deleted")

import logging
from uuid import UUID

from app.application.project.project_dto import ProjectDTO, ProjectCreateDTO, ProjectUpdateDTO
from app.application.common.exceptions import ResourceNotFoundError
from app.application.common.sentinel import UNSET
from app.application.common.pagination import Page, PageParams
from app.application.common.interfaces import IProjectRepo

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self, project_repo: IProjectRepo):
        self.repo = project_repo

    async def get_user_projects(
        self, user_id: UUID, page: PageParams = PageParams()
    ) -> Page[ProjectDTO]:
        rows, total = await self.repo.get_user_projects_with_stats(
            user_id, limit=page.limit, offset=page.offset
        )
        items = []
        for project, folders_count, snippets_count in rows:
            dto = ProjectDTO.model_validate(project)
            dto.folders_count = folders_count
            dto.snippets_count = snippets_count
            items.append(dto)
        return Page(items=items, total=total, limit=page.limit, offset=page.offset)

    async def get_project(self, project_id: UUID, user_id: UUID) -> ProjectDTO:
        project = await self.repo.get_project_by_id(project_id, user_id)
        if not project:
            raise ResourceNotFoundError(f"Project {project_id} not found")
        folders_count, snippets_count = await self.repo.get_project_stats(project.id)
        dto = ProjectDTO.model_validate(project)
        dto.folders_count = folders_count
        dto.snippets_count = snippets_count
        return dto

    async def create_project(self, user_id: UUID, data: ProjectCreateDTO) -> ProjectDTO:
        project = await self.repo.create_project(
            user_id=user_id, title=data.name, description=data.description
        )
        logger.info(f"Project {project.id} created for user {user_id}")
        return ProjectDTO.model_validate(project)

    async def update_project(
        self, project_id: UUID, user_id: UUID, data: ProjectUpdateDTO
    ) -> ProjectDTO:
        project = await self.repo.get_project_by_id(project_id, user_id)
        if not project:
            raise ResourceNotFoundError(f"Project {project_id} not found")
        fields = data.model_fields_set
        project = await self.repo.update_project(
            project,
            title=data.name if "name" in fields else UNSET,
            description=data.description if "description" in fields else UNSET,
        )
        logger.info(f"Project {project.id} updated")
        return ProjectDTO.model_validate(project)

    async def delete_project(self, project_id: UUID, user_id: UUID) -> None:
        project = await self.repo.get_project_by_id(project_id, user_id)
        if not project:
            raise ResourceNotFoundError(f"Project {project_id} not found")
        await self.repo.delete_project(project)
        logger.info(f"Project {project_id} deleted")

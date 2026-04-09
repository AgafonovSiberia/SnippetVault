from typing import Any, AsyncGenerator

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.infrastructure.repo.project_repo import ProjectRepo
from app.infrastructure.repo.folder_repo import FolderRepo
from app.infrastructure.repo.snippet_repo import SnippetRepo
from app.infrastructure.repo.auth_repo import AuthRepo
from app.application.auth.auth_service import AuthService
from app.core.config import config
from app.infrastructure.auth.providers import YandexOAuthProvider
from app.infrastructure.database.db import session_factory
from app.application.project.project_service import ProjectService
from app.application.project.folder_service import FolderService
from app.application.project.snippet_service import SnippetService
from app.api.auth_provider import AuthProvider

# Реэкспортируем для роутеров
from app.api.auth_provider import CurrentUser, AuthenticatedUser  # noqa: F401


class DatabaseProvider(FastapiProvider):
    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        async with session_factory() as session:
            async with session.begin():
                yield session


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_yandex_provider(self) -> YandexOAuthProvider:
        return YandexOAuthProvider(
            client_id=config.provider.YANDEX_CLIENT_ID,
            client_secret=config.provider.YANDEX_CLIENT_SECRET,
        )


class RepositoryProvider(FastapiProvider):
    @provide(scope=Scope.REQUEST)
    async def get_auth_repo(self, session: AsyncSession) -> AuthRepo:
        return AuthRepo(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_project_repo(self, session: AsyncSession) -> ProjectRepo:
        return ProjectRepo(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_folder_repo(self, session: AsyncSession) -> FolderRepo:
        return FolderRepo(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_snippet_repo(self, session: AsyncSession) -> SnippetRepo:
        return SnippetRepo(session=session)


class ServiceProvider(FastapiProvider):
    @provide(scope=Scope.REQUEST)
    async def get_auth_service(
        self, auth_repo: AuthRepo, yandex_provider: YandexOAuthProvider
    ) -> AuthService:
        return AuthService(auth_repo=auth_repo, yandex_provider=yandex_provider)

    @provide(scope=Scope.REQUEST)
    async def get_project_service(self, project_repo: ProjectRepo) -> ProjectService:
        return ProjectService(project_repo=project_repo)

    @provide(scope=Scope.REQUEST)
    async def get_folder_service(
        self, project_repo: ProjectRepo, folder_repo: FolderRepo
    ) -> FolderService:
        return FolderService(project_repo=project_repo, folder_repo=folder_repo)

    @provide(scope=Scope.REQUEST)
    async def get_snippet_service(
        self, project_repo: ProjectRepo, folder_repo: FolderRepo, snippet_repo: SnippetRepo
    ) -> SnippetService:
        return SnippetService(
            project_repo=project_repo,
            folder_repo=folder_repo,
            snippet_repo=snippet_repo,
        )


def create_container() -> AsyncContainer:
    return make_async_container(
        DatabaseProvider(),
        SettingsProvider(),
        RepositoryProvider(),
        ServiceProvider(),
        AuthProvider(),
    )

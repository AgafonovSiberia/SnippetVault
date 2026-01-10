from typing import Annotated, Any, AsyncGenerator
from uuid import UUID

from dishka import AsyncContainer, Provider, Scope, from_context, make_async_container, provide
from dishka.integrations.fastapi import FastapiProvider
from fastapi import Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.application.auth.auth_dto import UserDTO
from app.application.auth.auth_service import AuthService
from app.core.config import config
from app.core.secure import decode_token
from app.infrastructure.auth.providers import YandexOAuthProvider
from app.infrastructure.database.db import session_factory
from app.infrastructure.repo.auth_repo import AuthRepo
from app.application.common.exceptions import AuthenticationError

CurrentUser = Annotated[UserDTO | None, "current_user"]
AuthenticatedUser = Annotated[UserDTO, "authenticated_user"]


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


class ServiceProvider(FastapiProvider):
    @provide(scope=Scope.REQUEST)
    async def get_auth_service(
            self, auth_repo: AuthRepo, yandex_provider: YandexOAuthProvider
    ) -> AuthService:
        return AuthService(auth_repo=auth_repo, yandex_provider=yandex_provider)


class AuthProvider(FastapiProvider):
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
            self, request: Request, auth_service: AuthService
    ) -> CurrentUser:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.removeprefix("Bearer ")
        payload = decode_token(token)

        if not payload or payload.get("type") != "access":
            return None

        user_id_str = payload.get("sub")
        if not user_id_str:
            return None

        try:
            user_id = UUID(user_id_str)
        except ValueError:
            return None

        try:
            user = await auth_service.get_current_user(user_id)
            return user
        except Exception:
            return None

    @provide(scope=Scope.REQUEST)
    async def get_authenticated_user(self, user: CurrentUser) -> AuthenticatedUser:
        if user is None:
            raise AuthenticationError("Authentication required")
        return user


def create_container() -> AsyncContainer:
    container = make_async_container(
        DatabaseProvider(),
        SettingsProvider(),
        RepositoryProvider(),
        ServiceProvider(),
        AuthProvider(),
    )
    return container

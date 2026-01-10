import logging
from uuid import UUID

from app.application.auth.auth_dto import AuthResponseDTO, AuthTokensDTO, UserDTO
from app.application.common.exceptions import InvalidTokenError, UserNotFoundError
from app.core.secure import create_access_token, create_refresh_token, decode_token
from app.infrastructure.auth.providers import YandexOAuthProvider
from app.infrastructure.repo.auth_repo import AuthRepo

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, auth_repo: AuthRepo, yandex_provider: YandexOAuthProvider):
        self.auth_repo = auth_repo
        self.yandex_provider = yandex_provider

    async def authenticate_yandex(self, token: str) -> AuthResponseDTO:
        user_info = await self.yandex_provider.get_user_info(token)

        provider_user_id, display_name, avatar_url = (
            self.yandex_provider.extract_user_data(user_info)
        )

        logger.info(f"Yandex user authenticated: {provider_user_id}")

        user = await self.auth_repo.get_user_by_provider("yandex", provider_user_id)

        if not user:
            logger.info(f"Creating new user for Yandex ID: {provider_user_id}")
            user = await self.auth_repo.create_user(
                display_name=display_name, avatar_url=avatar_url
            )
            await self.auth_repo.create_auth_account(
                user_id=user.id,
                provider="yandex",
                provider_user_id=provider_user_id,
                provider_payload=user_info,
            )
        else:
            if user.display_name != display_name or user.avatar_url != avatar_url:
                logger.info(f"Updating user info for user: {user.id}")
                await self.auth_repo.update_user(
                    user_id=user.id,
                    display_name=display_name,
                    avatar_url=avatar_url,
                )
                user = await self.auth_repo.get_user_by_id(user.id)

        at = create_access_token(str(user.id))
        rt = create_refresh_token(str(user.id))

        return AuthResponseDTO(
            user=UserDTO.model_validate(user),
            tokens=AuthTokensDTO(access_token=at, refresh_token=rt),
        )

    async def refresh_access_token(self, refresh_token: str) -> str:
        payload = decode_token(refresh_token)

        if not payload:
            raise InvalidTokenError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Token is not a refresh token")

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise InvalidTokenError("Invalid token payload")

        try:
            user_id = UUID(user_id_str)
        except ValueError:
            raise InvalidTokenError("Invalid user ID in token")

        user = await self.auth_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        logger.info(f"Refreshing access token for user: {user.id}")
        new_access_token = create_access_token(str(user.id))
        return new_access_token

    async def get_current_user(self, user_id: UUID) -> UserDTO:
        user = await self.auth_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        return UserDTO.model_validate(user)

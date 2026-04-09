from typing import NewType
from uuid import UUID

from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FastapiProvider
from fastapi import HTTPException, Request, status

from app.application.auth.auth_dto import UserDTO
from app.application.auth.auth_service import AuthService
from app.application.common.exceptions import UserNotFoundError
from app.core.secure import decode_token

# Используются как отдельные типы для Dishka DI
AuthenticatedUser = NewType("AuthenticatedUser", UserDTO)
CurrentUser = NewType("CurrentUser", UserDTO)


class AuthProvider(FastapiProvider):
    @provide(scope=Scope.REQUEST, provides=AuthenticatedUser)
    async def get_authenticated_user(
        self,
        request: Request,
        auth_service: AuthService,
    ) -> AuthenticatedUser:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = auth_header[7:]
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            user_id = UUID(payload["sub"])
        except (KeyError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        try:
            user = await auth_service.get_current_user(user_id)
        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return AuthenticatedUser(user)

    @provide(scope=Scope.REQUEST, provides=CurrentUser)
    async def get_current_user_optional(
        self,
        request: Request,
        auth_service: AuthService,
    ) -> CurrentUser:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header[7:]
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return None
        try:
            user_id = UUID(payload["sub"])
            user = await auth_service.get_current_user(user_id)
            return CurrentUser(user)
        except (KeyError, ValueError, UserNotFoundError):
            return None

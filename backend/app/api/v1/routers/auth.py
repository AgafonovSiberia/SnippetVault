import logging

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Cookie, HTTPException, Response, status

from app.api.shemas.auth import AuthResponse, TokenResponse, UserResponse, YandexAuthRequest
from app.application.auth.auth_service import AuthService
from app.di import AuthenticatedUser

logger = logging.getLogger(__name__)

router = APIRouter(route_class=DishkaRoute, prefix="/auth", tags=["Authentication"])


@router.get("/", status_code=status.HTTP_200_OK)
async def root() -> dict:
    return {"message": "Hello, world!"}


@router.post("/yandex", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def yandex_auth(
        auth_data: YandexAuthRequest,
        response: Response,
        auth_service: FromDishka[AuthService],
) -> AuthResponse:
    logger.info("Processing Yandex ID Suggest authentication")

    auth_result = await auth_service.authenticate_yandex(auth_data.token)

    response.set_cookie(
        key="refresh_token",
        value=auth_result.tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=2592000,
    )

    return AuthResponse(
        user=UserResponse.model_validate(auth_result.user),
        access_token=auth_result.tokens.access_token,
        token_type=auth_result.tokens.token_type,
    )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
        auth_service: FromDishka[AuthService],
        refresh_token: str = Cookie(None),
) -> TokenResponse:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    logger.info("Refreshing access token")
    new_access_token = await auth_service.refresh_access_token(refresh_token)

    return TokenResponse(access_token=new_access_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response) -> dict:
    logger.info("User logging out")
    response.delete_cookie("refresh_token")
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_info(
        current_user: FromDishka[AuthenticatedUser],
) -> UserResponse:
    return UserResponse.model_validate(current_user)

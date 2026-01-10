import httpx
from app.application.common.exceptions import InvalidTokenError, YandexServiceError


class YandexOAuthProvider:
    USER_INFO_URL = "https://login.yandex.ru/info"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    async def get_user_info(self, access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"OAuth {access_token}"}
            try:
                resp = await client.get(self.USER_INFO_URL, headers=headers, timeout=10.0)
                resp.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise InvalidTokenError(f"Invalid Yandex token: {e.response.text}")
                raise YandexServiceError(f"Yandex API error: {e.response.text}")
            except httpx.RequestError as e:
                raise YandexServiceError(f"Yandex service unavailable: {str(e)}")

            return resp.json()

    def extract_user_data(self, user_info: dict) -> tuple[str, str | None, str | None]:
        yandex_id = str(user_info.get("id"))
        display_name = (
                user_info.get("display_name")
                or user_info.get("real_name")
                or user_info.get("login")
        )

        avatar_id = user_info.get("default_avatar_id")
        avatar_url = (
            f"https://avatars.yandex.net/get-yapic/{avatar_id}/islands-200"
            if avatar_id
            else None
        )

        return yandex_id, display_name, avatar_url

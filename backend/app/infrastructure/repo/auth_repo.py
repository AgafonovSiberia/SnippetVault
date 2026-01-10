from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.infrastructure.database.models import AuthAccount, User


class AuthRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_provider(self, provider: str, provider_user_id: str) -> User | None:
        stmt = (
            select(User)
            .join(AuthAccount)
            .where(
                AuthAccount.provider == provider,
                AuthAccount.provider_user_id == provider_user_id,
            )
            .options(selectinload(User.accounts))
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_auth_account(
            self, provider: str, provider_user_id: str
    ) -> AuthAccount | None:
        stmt = select(AuthAccount).where(
            AuthAccount.provider == provider,
            AuthAccount.provider_user_id == provider_user_id,
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def create_user(
            self,
            display_name: str | None = None,
            avatar_url: str | None = None,
    ) -> User:
        user = User(display_name=display_name, avatar_url=avatar_url)
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def create_auth_account(
            self,
            user_id: UUID,
            provider: str,
            provider_user_id: str,
            provider_payload: dict | None = None,
    ) -> AuthAccount:
        account = AuthAccount(
            user_id=user_id,
            provider=provider,
            provider_user_id=provider_user_id,
            provider_payload=provider_payload,
        )
        self._session.add(account)
        await self._session.flush()
        await self._session.refresh(account)
        return account

    async def update_user(
            self,
            user_id: UUID,
            display_name: str | None = None,
            avatar_url: str | None = None,
    ) -> User | None:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        if display_name is not None:
            user.display_name = display_name
        if avatar_url is not None:
            user.avatar_url = avatar_url

        await self._session.flush()
        await self._session.refresh(user)
        return user

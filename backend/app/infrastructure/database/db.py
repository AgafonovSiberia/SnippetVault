from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import config

engine = create_async_engine(
    str(config.database.DB_URL), echo=False, pool_pre_ping=True
)
session_factory = async_sessionmaker(
    engine, autoflush=True, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass

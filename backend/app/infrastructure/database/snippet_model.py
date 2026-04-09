import uuid
from datetime import datetime, UTC

from sqlalchemy import String, Text, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.db import Base


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint("user_id", "normalized_name", name="uq_user_tag"),
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    normalized_name: Mapped[str] = mapped_column(String(100))


class SnippetTag(Base):
    __tablename__ = "snippet_tags"

    snippet_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("snippets.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )


class Snippet(Base):
    __tablename__ = "snippets"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    folder_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("folders.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="snippet_tags",
        lazy="selectin",
    )

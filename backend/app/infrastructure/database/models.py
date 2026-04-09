# Единая точка импорта всех ORM-моделей.
# Alembic и репозитории импортируют отсюда.
# Модели разбиты по доменам в отдельных файлах рядом.

from app.infrastructure.database.user_model import User, AuthAccount  # noqa: F401
from app.infrastructure.database.project_model import Project, Folder  # noqa: F401
from app.infrastructure.database.snippet_model import Tag, SnippetTag, Snippet  # noqa: F401

__all__ = ["User", "AuthAccount", "Project", "Folder", "Tag", "SnippetTag", "Snippet"]

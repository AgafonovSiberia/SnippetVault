from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class PageParams:
    limit: int = 50
    offset: int = 0

    def __init__(self, limit: int = 50, offset: int = 0):
        self.limit = max(1, min(limit, 200))
        self.offset = max(0, offset)


@dataclass
class Page(Generic[T]):
    items: list[T] = field(default_factory=list)
    total: int = 0
    limit: int = 50
    offset: int = 0

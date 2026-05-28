from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserModel:
    user_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_admin: bool = False
    is_banned: bool = False
    registration_date: datetime | None = None
    query_count: int = 0

    def full_name(self) -> str:
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return ' '.join(parts) if parts else str(self.user_id)


@dataclass
class QueryModel:
    user_id: int
    query_text: str
    query_id: int | None = None
    query_date: datetime | None = None
    user: UserModel | None = None


@dataclass
class Pagination:
    page: int
    per_page: int
    total_items: int
    total_pages: int

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

from aiogram.filters import BaseFilter
from aiogram.types import Message

from db.models import UserModel


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, user_row: UserModel | None = None) -> bool:
        return user_row is not None and user_row.is_admin

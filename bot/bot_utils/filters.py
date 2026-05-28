from aiogram.filters import BaseFilter
from aiogram.types import Message

from DB.models import UserModel
from DB.tables.users import UsersTable


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        with UsersTable() as users_db:
            user: UserModel | None = users_db.get_user(message.from_user.id)
            if user:
                return user.is_admin
            return False

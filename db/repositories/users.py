from pathlib import Path

from db.models import Pagination, UserModel
from db.tables.users import UsersTable


class UsersRepository:
    def __init__(self, db_path: Path):
        self._db_path = db_path

    def get_user(self, user_id: int) -> UserModel | None:
        with UsersTable(self._db_path) as t:
            return t.get_user(user_id)

    def add_user(self, user: UserModel) -> UserModel:
        with UsersTable(self._db_path) as t:
            return t.add_user(user)

    def update_user(self, user: UserModel) -> UserModel | None:
        with UsersTable(self._db_path) as t:
            return t.update_user(user)

    def delete_user(self, user_id: int) -> bool:
        with UsersTable(self._db_path) as t:
            return t.delete_user(user_id)

    def is_exists(self, user_id: int) -> bool:
        with UsersTable(self._db_path) as t:
            return t.is_exists(user_id)

    def set_admin(self, user_id: int, set_by: int, is_admin: bool = True) -> bool:
        with UsersTable(self._db_path) as t:
            return t.set_admin(user_id, set_by, is_admin)

    def set_ban_status(self, user_id: int, banned_by: int, ban: bool = True) -> bool:
        with UsersTable(self._db_path) as t:
            return t.set_ban_status(user_id, banned_by, ban)

    def get_all_users(self, page: int = 1, per_page: int = 10) -> tuple[list[UserModel], Pagination]:
        with UsersTable(self._db_path) as t:
            return t.get_all_users(page, per_page)

    def get_admins(self) -> list[UserModel]:
        with UsersTable(self._db_path) as t:
            return t.get_admins()

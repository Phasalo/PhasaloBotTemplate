from pathlib import Path

from db.repositories.queries import QueriesRepository
from db.repositories.users import UsersRepository
from db.tables.queries import QueriesTable
from db.tables.users import UsersTable

__all__ = [
    'QueriesRepository',
    'UsersRepository',
    'init_database',
]


def init_database(db_path: Path) -> None:
    with UsersTable(db_path) as users_db:
        users_db.create_table()

    with QueriesTable(db_path) as queries_db:
        queries_db.create_table()

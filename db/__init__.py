from pathlib import Path

from db.repositories import QueriesRepository, UsersRepository
from db.tables import QueriesTable, UsersTable

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

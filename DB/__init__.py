from DB.tables.queries import QueriesTable
from DB.tables.users import UsersTable


def init_database():
    with UsersTable() as users_db:
        users_db.create_table()

    with QueriesTable() as queries_db:
        queries_db.create_table()

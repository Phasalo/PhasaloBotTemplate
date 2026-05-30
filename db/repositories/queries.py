from pathlib import Path

from db.models import Pagination, QueryModel
from db.tables.queries import QueriesTable


class QueriesRepository:
    def __init__(self, db_path: Path):
        self._db_path = db_path

    def add_query(self, query: QueryModel) -> QueryModel:
        with QueriesTable(self._db_path) as t:
            return t.add_query(query)

    def get_query(self, query_id: int) -> QueryModel | None:
        with QueriesTable(self._db_path) as t:
            return t.get_query(query_id)

    def get_user_queries(self, user_id: int, page: int = 1, per_page: int = 10) -> tuple[list[QueryModel], Pagination]:
        with QueriesTable(self._db_path) as t:
            return t.get_user_queries(user_id, page, per_page)

    def get_last_queries(self, amount: int = 5) -> list[QueryModel]:
        with QueriesTable(self._db_path) as t:
            return t.get_last_queries(amount)

    def get_all_queries(self, limit: int | None = None) -> list[QueryModel]:
        with QueriesTable(self._db_path) as t:
            return t.get_all_queries(limit)

    def delete_query(self, query_id: int) -> bool:
        with QueriesTable(self._db_path) as t:
            return t.delete_query(query_id)

    def delete_user_queries(self, user_id: int) -> int:
        with QueriesTable(self._db_path) as t:
            return t.delete_user_queries(user_id)

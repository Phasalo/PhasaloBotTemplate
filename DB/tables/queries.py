from datetime import datetime, timedelta

from DB.models import Pagination, QueryModel, UserModel
from DB.tables.base import BaseTable
from utils.format_string import clear_string


class QueriesTable(BaseTable):
    __tablename__ = 'queries'

    def create_table(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.__tablename__} (
            query_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query_text TEXT NOT NULL,
            query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )""")
        self.cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_user_queries ON {self.__tablename__}(user_id)')
        self.conn.commit()
        self._log('CREATE_TABLE')

    def add_query(self, query: QueryModel) -> QueryModel:
        self.cursor.execute(
            f"""
        INSERT INTO {self.__tablename__} (user_id, query_text)
        VALUES (?, ?)""",
            (query.user_id, clear_string(query.query_text)),
        )
        query_id = self.cursor.lastrowid
        self.conn.commit()
        self._log('ADD_QUERY', query_id=query_id, user_id=query.user_id)
        return self.get_query(query_id)

    def get_query(self, query_id: int) -> QueryModel | None:
        self.cursor.execute(
            f"""
        SELECT q.query_id, q.user_id, q.query_text, q.query_date,
               u.username, u.first_name, u.last_name, u.is_admin
        FROM {self.__tablename__} q
        LEFT JOIN users u ON q.user_id = u.user_id
        WHERE q.query_id = ?""",
            (query_id,),
        )
        row = self.cursor.fetchone()
        if row:
            user = (
                UserModel(
                    user_id=row['user_id'],
                    username=row['username'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    is_admin=bool(row['is_admin']),
                )
                if row['user_id']
                else None
            )

            return QueryModel(
                query_id=row['query_id'],
                user_id=row['user_id'],
                query_text=row['query_text'],
                query_date=(
                    datetime.fromisoformat(row['query_date']) + timedelta(hours=3) if row['query_date'] else None
                ),
                user=user,
            )
        return None

    def get_user_queries(self, user_id: int, page: int = 1, per_page: int = 10) -> tuple[list[QueryModel], Pagination]:
        pagination = Pagination(page=page, per_page=per_page, total_items=0, total_pages=0)

        self.cursor.execute(
            f"""
            SELECT
                q.query_id, q.user_id, q.query_text, q.query_date,
                u.username, u.first_name, u.last_name, u.is_admin
            FROM {self.__tablename__} q
            LEFT JOIN users u ON q.user_id = u.user_id
            WHERE q.user_id = ?
            ORDER BY q.query_date DESC
            LIMIT ? OFFSET ?
        """,
            (user_id, pagination.per_page, pagination.offset),
        )

        queries = [
            QueryModel(
                query_id=row['query_id'],
                user_id=row['user_id'],
                query_text=row['query_text'],
                query_date=(
                    datetime.fromisoformat(row['query_date']) + timedelta(hours=3) if row['query_date'] else None
                ),
                user=UserModel(
                    user_id=row['user_id'],
                    username=row['username'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    is_admin=bool(row['is_admin']),
                ),
            )
            for row in self.cursor
        ]

        self.cursor.execute(f'SELECT COUNT(*) as total FROM {self.__tablename__} WHERE user_id = ?', (user_id,))
        total_queries = self.cursor.fetchone()['total']

        pagination.total_items = total_queries
        pagination.total_pages = (total_queries + per_page - 1) // per_page

        return queries, pagination

    def get_all_queries(self, limit: int | None = None) -> list[QueryModel]:
        query = f"""
        SELECT q.query_id, q.user_id, q.query_text, q.query_date,
               u.username, u.first_name, u.last_name, u.is_admin
        FROM {self.__tablename__} q
        LEFT JOIN users u ON q.user_id = u.user_id
        ORDER BY q.query_date DESC"""

        params = ()
        if limit:
            query += ' LIMIT ?'
            params = (limit,)

        self.cursor.execute(query, params)
        return [
            QueryModel(
                query_id=row['query_id'],
                user_id=row['user_id'],
                query_text=row['query_text'],
                query_date=(
                    datetime.fromisoformat(row['query_date']) + timedelta(hours=3) if row['query_date'] else None
                ),
                user=UserModel(
                    user_id=row['user_id'],
                    username=row['username'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    is_admin=bool(row['is_admin']),
                )
                if row['user_id']
                else None,
            )
            for row in self.cursor
        ]

    def get_last_queries(self, amount: int = 5) -> list[QueryModel]:
        if amount < 0:
            raise ValueError('Amount cannot be negative')

        return self.get_all_queries(limit=amount)

    def delete_query(self, query_id: int) -> bool:
        self.cursor.execute(f'DELETE FROM {self.__tablename__} WHERE query_id = ?', (query_id,))
        self.conn.commit()
        deleted = self.cursor.rowcount > 0
        if deleted:
            self._log('DELETE_QUERY', query_id=query_id)
        return deleted

    def delete_user_queries(self, user_id: int) -> int:
        self.cursor.execute(f'DELETE FROM {self.__tablename__} WHERE user_id = ?', (user_id,))
        self.conn.commit()
        deleted_count = self.cursor.rowcount
        if deleted_count > 0:
            self._log('DELETE_USER_QUERIES', user_id=user_id, count=deleted_count)
        return deleted_count

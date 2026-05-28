import logging
import os
import sqlite3
from typing import Any

logger = logging.getLogger(__name__)


class BaseTable:
    __tablename__: str

    def __init__(self, db_name: str = f'{os.path.dirname(__file__)}/users.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
        self.conn = None
        self.cursor = None

    def _log(self, action: str, **kwargs: Any):
        logger.info(
            "Table='%s', Action='%s', Details: %s",
            self.__tablename__,
            action,
            ', '.join(f'{k}={v}' for k, v in kwargs.items()),
        )

    @property
    def tablename(self) -> str:
        return self.__tablename__

import sqlite3

from abc import ABC, abstractmethod


class Database(ABC):

    def __init__(self, path: str, table_name: str):
        self._path = path
        self._table_name = table_name
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self._path)

    @abstractmethod
    def _create_table(self):
        pass

    def clear(self):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'DELETE * FROM {self._table_name}')

        conn.commit()
        conn.close()

    def get_all_items(self):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM {self._table_name}')
        items = cur.fetchall()

        conn.commit()
        conn.close()

        return items

    def get_last_added_item(self):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM {self._table_name} ORDER BY id DESC LIMIT 1')
        items = cur.fetchone()

        conn.commit()
        conn.close()

        return items

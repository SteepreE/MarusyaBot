import sqlite3


class Database:

    def __init__(self, path):
        self._path = path

    def get_connection(self):
        return sqlite3.connect(self._path)

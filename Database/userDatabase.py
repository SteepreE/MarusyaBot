from Database.database import Database


class UserDatabase(Database):

    def __init__(self, path: str):
        super().__init__(path, 'users')

    def _create_table(self):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS {self._table_name}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, phone TEXT)''')

        conn.commit()
        conn.close()

    def find_user_by_name(self, name: str):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'''SELECT * FROM {self._table_name} WHERE name=? ''', (name, ))

        result = cur.fetchone()

        conn.close()

        return result

    def find_user_by_id(self, user_id):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'''SELECT * FROM {self._table_name} WHERE id={user_id} ''')

        result = cur.fetchone()

        conn.close()

        return result

    def add_user(self, name, phone):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'''INSERT INTO {self._table_name} (name, phone)
                    VALUES (?,?)''', (name, phone))

        conn.commit()
        conn.close()

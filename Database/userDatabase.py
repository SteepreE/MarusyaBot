from Database.database import Database


class UserDatabase(Database):

    def __init__(self, path: str):
        super().__init__(path, 'users')

    def _create_table(self):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS {self._table_name}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    first_name TEXT, second_name TEXT, third_name TEXT)''')

        conn.commit()
        conn.close()

    def find_user_by_name(self, first_name, second_name, third_name):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'''SELECT * FROM {self._table_name} 
                    WHERE first_name=? AND second_name=? AND third_name=?''',
                    (first_name, second_name, third_name))

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

    def add_user(self, first_name, second_name, third_name):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'''INSERT INTO {self._table_name} (first_name, second_name, third_name)
                    VALUES (?,?,?)''', (first_name, second_name, third_name))

        conn.commit()
        conn.close()

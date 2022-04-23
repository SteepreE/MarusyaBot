from Database.database import Database

ORDERS_LIMIT = 2


class OrdersDatabase(Database):

    def __init__(self, path: str):
        super().__init__(path, 'orders')

    def _create_table(self):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS {self._table_name}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, product TEXT, sizes TEXT,
                    start_date TEXT, finish_date TEXT, stage TEXT, price_info TEXT)''')

        conn.commit()
        conn.close()

    def add_order(self, user_id: int, sizes: str, product: str,
                  start_date: str, finish_date: str, stage: str, price_info: str):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'''INSERT INTO {self._table_name} 
                    (user_id, product, sizes, start_date, finish_date, stage, price_info)
                    VALUES (?,?,?,?,?,?,?)''',
                    (user_id, product, sizes, start_date, finish_date, stage, price_info))

        conn.commit()
        conn.close()

    def get_orders_by_offset(self, offset):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM {self._table_name} LIMIT {ORDERS_LIMIT} OFFSET {offset * ORDERS_LIMIT}')
        result = cur.fetchall()

        conn.close()

        return result

    def delete_order(self, order_id: int):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'DELETE FROM {self._table_name} WHERE id={order_id}')

        conn.commit()
        conn.close()

    def edit_order(self):
        pass

    def find_order_by_id(self, order_id: int):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM {self._table_name} WHERE id={order_id}')
        result = cur.fetchone()

        conn.close()

        return result

    def find_orders_by_user_id(self, user_id: int):
        conn = self._get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM {self._table_name} WHERE user_id={user_id}')
        result = cur.fetchall()

        conn.close()

        return result

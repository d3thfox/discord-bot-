import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path
        self.create_table()  # Автоматически создаем таблицу при инициализации

    def create_table(self):
        """Создает таблицу users в базе данных"""
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    nick_name TEXT NOT NULL,
                    coins INTEGER DEFAULT 0,
                    last_reward_time TIMESTAMP
                )
            """)
            conn.commit()
    def add_user(self, nick_name : str , user_id : int):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO users (nick_name, user_id) VALUES (?, ?)",
                (nick_name,user_id)
            )
            conn.commit()

    def get_balance(self, user_id: int) -> int:
     """Возвращает текущий баланс пользователя"""
     with sqlite3.connect(self.path) as conn:
        cursor = conn.execute(
            "SELECT coins FROM users WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else 0

    def update_coins(self, user_id: int, amount: int) -> bool:
        """Изменяет баланс на указанное количество (может быть отрицательным)"""
        try:
            with sqlite3.connect(self.path) as conn:
                conn.execute(
                    "UPDATE users SET coins = coins + ? WHERE user_id = ?",
                    (amount, user_id)
                )
                conn.commit()
            return True
        except sqlite3.Error:
            return False
        


            


        
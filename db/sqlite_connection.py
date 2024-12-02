import sqlite3
from models import client


class Database:
    def __init__(self, db_file) -> None:

        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cbdt()

    def cbdt(self):
        with self.connection:
            create = """ CREATE TABLE IF NOT EXISTS Users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL UNIQUE ON CONFLICT IGNORE,
                    full_name TEXT,
                    vk_access_token TEXT DEFAULT NONE,
                    username TEXT);
                    CREATE TABLE IF NOT EXISTS Telegram_groups
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL UNIQUE ON CONFLICT IGNORE,
                    vk_group_id TEXT,
                    vk_group_name TEXT,
                    username TEXT,
                    chat_id TEXT,
                    user_telegram_id INTEGER
                    );
                    """
            self.cursor.executescript(create)

            # CREATE TABLE IF NOT EXISTS Vk_groups
            # (id INTEGER PRIMARY KEY AUTOINCREMENT,
            # group_id INTEGER NOT NULL UNIQUE ON CONFLICT IGNORE,
            # );

    def add_user(self, telegram_id, full_name, username):
        with self.connection:
            self.cursor.execute(
                f"INSERT OR IGNORE INTO Users(telegram_id,full_name, username) VALUES(?,?,?)", (telegram_id, full_name, username))

    def get_chat_data(self, chat_id) -> client.Telegram_group:
        with self.connection:
            group = self.cursor.execute(
                f"SELECT * FROM Telegram_groups WHERE chat_id=?", (str(chat_id),))
            return client.Telegram_group(*group.fetchone())

    def get_user(self, telegram_id) -> client.User:
        with self.connection:
            group = self.cursor.execute(
                f"SELECT * FROM Users WHERE telegram_id=?", (telegram_id,))
            return client.User(*group.fetchone())

    def get_all_user_tg_groups(self, telegram_id):
        with self.connection:
            groups = self.cursor.execute(
                f"SELECT * FROM Telegram_groups WHERE telegram_id=?", (telegram_id,))
            result = [client.Telegram_group(*group)
                      for group in groups.fetchall()]

            return result

    def set_vk_data_to_rg_group(self, data):
        with self.connection:
            self.cursor.execute(
                f"UPDATE Telegram_groups SET vk_group_id=?, vk_group_name=? WHERE id=?",
                (data["id"], data["name"], data["telegram_group_id"]))

    def update_access_token(self, telegram_id, token):
        with self.connection:
            self.cursor.execute(
                f"UPDATE Users SET vk_access_token=? WHERE telegram_id=?", (token, telegram_id))

    def add_tg_chat(self, telegram_id, username, chat_id):
        with self.connection:
            self.cursor.execute(
                f"INSERT OR IGNORE INTO Telegram_groups(telegram_id,username, chat_id) VALUES(?,?,?)", (telegram_id, username, chat_id))

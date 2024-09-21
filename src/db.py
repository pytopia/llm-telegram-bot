import sqlite3
from datetime import datetime, timedelta

from pytz import timezone

TIMEZONE = timezone("UTC")

class UserDatabase:
    def __init__(self, db_name="src/user.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.cursor.close()
            self.conn.close()
        return False

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            is_authorized BOOLEAN,
            rate_limit INTEGER
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            timestamp DATETIME,
            FOREIGN KEY (username) REFERENCES users (username)
        )
        """)

    def get_all_users(self):
        self.cursor.execute("SELECT username, is_authorized, rate_limit FROM users")
        return self.cursor.fetchall()

    def add_user(self, username, is_authorized=True, rate_limit=100):
        self.cursor.execute(
            """
        INSERT OR REPLACE INTO users (username, is_authorized, rate_limit)
        VALUES (?, ?, ?)
        """,
            (username, is_authorized, rate_limit),
        )

    def delete_user(self, username):
        self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))

    def is_user_authorized(self, username):
        self.cursor.execute("SELECT is_authorized FROM users WHERE username = ? and is_authorized = 1", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else False

    def get_user_rate_limit(self, username):
        self.cursor.execute("SELECT rate_limit FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def log_request(self, username):
        current_time = datetime.now(tz=TIMEZONE)
        self.cursor.execute("INSERT INTO requests (username, timestamp) VALUES (?, ?)", (username, current_time))

    def is_rate_limited(self, username):
        rate_limit = self.get_user_rate_limit(username)
        if rate_limit is None:
            return True

        request_count = self.get_user_request_count(username)
        return request_count >= rate_limit

    def get_user_request_count(self, username):
        one_day_ago = datetime.now(tz=TIMEZONE) - timedelta(days=1)
        self.cursor.execute(
            """
        SELECT COUNT(*) FROM requests
        WHERE username = ? AND timestamp > ?
        """,
            (username, one_day_ago),
        )

        return self.cursor.fetchone()[0] or 0

import sqlite3

class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_active_users(self):
        with self.connection:
            sql = "SELECT * FROM users WHERE active = ?"
            users = self.cursor.execute(sql, [True])
            return users

    def user_exists(self, user_id):
        with self.connection:
            sql = "SELECT * FROM users WHERE user_id = ?"
            user = self.cursor.execute(sql, [user_id]).fetchall()
            if user:
                return True
            else:
                return False

    def subscribe_user(self, user_id, schedule):
        with self.connection:
            sql = "INSERT INTO users (user_id, schedule) VALUES (?, ?)"
            user = self.cursor.execute(sql, [user_id, schedule])
            return user

    def unsubscribe_user(self, user_id):
        with self.connection:
            sql = "UPDATE users SET active = ? WHERE user_id = ?"
            user = self.cursor.execute(sql, [False, user_id])
            return user

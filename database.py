import sqlite3

class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_active_users(self):
        with self.connection:
            sql = "SELECT user_id, schedule FROM users WHERE active = ?"
            users = self.cursor.execute(sql, [True]).fetchall()
            return users

    def user_exists(self, user_id):
        with self.connection:
            sql = "SELECT * FROM users WHERE user_id = ?"
            user = self.cursor.execute(sql, [user_id]).fetchall()
            if len(user) == 0:
                return False

            user = user[0]
            if len(user) == 0:
                return False

            return True

    def is_active_user(self, user_id):
        with self.connection:
            sql = "SELECT active FROM users WHERE user_id = ?"
            active = self.cursor.execute(sql, [user_id]).fetchall()
            if len(active) == 0:
                return False

            active = active[0]
            if len(active) == 0:
                return False

            if active[0] == 0:
                return False

            return True

    def subscribe_user(self, user_id, schedule):
        with self.connection:
            sql = "INSERT INTO users (user_id, schedule, active) VALUES (?, ?, ?)"
            user = self.cursor.execute(sql, [user_id, schedule, True])
            return user

    def unsubscribe_user(self, user_id):
        with self.connection:
            sql = "UPDATE users SET active = ? WHERE user_id = ?"
            user = self.cursor.execute(sql, [False, user_id])
            return user

    def update_schedule(self, user_id, schedule):
        with self.connection:
            sql = "UPDATE users SET schedule = ?, active = ? WHERE user_id = ?"
            self.cursor.execute(sql, [schedule, True, user_id])

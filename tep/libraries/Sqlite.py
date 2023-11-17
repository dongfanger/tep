import os
import sqlite3

from tep.libraries.Config import Config


class Sqlite:
    DB_FILE = "sqlite3.db"

    @staticmethod
    def execute(sql: str, data: tuple = None):
        os.chdir(Config.BASE_DIR)
        conn = sqlite3.connect(Sqlite.DB_FILE)
        if data:
            conn.execute(sql, data)
        else:
            conn.execute(sql)
        conn.commit()
        conn.close()

    @staticmethod
    def create_table_replay():
        Sqlite.execute("""CREATE TABLE IF NOT EXISTS replay
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   case_id TEXT NOT NULL,
                   request_order INTEGER NOT NULL,
                   method TEXT NOT NULL,
                   url TEXT NOT NULL,
                   expect TEXT NOT NULL,
                   actual TEXT)""")

    @staticmethod
    def insert_into_replay_expect(data: tuple):
        if not Sqlite.is_replay_existed(data):
            Sqlite.execute("INSERT INTO replay(case_id, request_order, method, url, expect) VALUES (?, ?, ?, ?, ?)", data)

    @staticmethod
    def is_replay_existed(data: tuple) -> bool:
        os.chdir(Config.BASE_DIR)
        conn = sqlite3.connect(Sqlite.DB_FILE)
        cursor = conn.cursor()
        where = data[:-1]
        cursor.execute("SELECT * FROM replay WHERE case_id = ? AND request_order = ? AND method = ? AND url = ?", where)
        results = cursor.fetchall()
        conn.close()
        if results:
            return True
        return False

    @staticmethod
    def update_replay_actual(data: tuple):
        Sqlite.execute("UPDATE replay SET actual = ? WHERE case_id = ? AND request_order = ? AND method = ? AND url = ?", data)

    @staticmethod
    def record_actual(data: tuple, var: dict):
        Sqlite.update_replay_actual(data)
        var["requestOrder"] += 1


    @staticmethod
    def get_expect_actual(case_id: str):
        os.chdir(Config.BASE_DIR)
        conn = sqlite3.connect(Sqlite.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT expect, actual, method, url FROM replay WHERE case_id = ?", (case_id,))
        results = cursor.fetchall()
        conn.close()
        return results

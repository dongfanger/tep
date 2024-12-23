import logging

import pymysql
import pytest


class Data:
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = "12345678"
    database = "sys"


@pytest.fixture(scope="session")
def mysql_execute():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="12345678", database="sys")

    def _function(sql: str):
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logging.error(f"Database execute error: {e}")
            conn.rollback()

        return cursor

    yield _function
    conn.close()  # After test, close connection

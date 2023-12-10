import pytest

from tep.libraries.DB import DB


@pytest.fixture(scope="session")
def mysql_execute(DbcKeyword):
    conn = DbcKeyword(host="127.0.0.1", port=3306, user="root", password="12345678", database="sys")

    def _function(sql: str):
        cursor = conn.cursor()
        DB.pymysql_execute(conn, cursor, sql)
        return cursor

    yield _function
    conn.close()  # After test, close connection

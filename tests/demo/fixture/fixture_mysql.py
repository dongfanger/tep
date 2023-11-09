import pytest

from tep.libraries.DB import DB
from tep.libraries.Result import Result


@pytest.fixture(scope="session")
def mysql_execute(DbcKeyword):
    ro = DbcKeyword(host="127.0.0.1", port=3306, user="root", password="12345678", database="sys")
    conn = ro.conn

    def _function(sql: str) -> Result:
        cursor = conn.cursor()
        DB.pymysql_execute(conn, cursor, sql)
        ro = Result()
        ro.cursor = cursor
        return ro

    yield _function
    conn.close()  # After test, close connection

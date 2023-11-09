import pymysql

from tep.libraries.Result import Result


def DbcImpl(host: str, port: int, user: str, password: str, database: str) -> Result:
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    result = Result()
    result.conn = conn
    return result

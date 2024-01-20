import pymysql


def DbcImpl(host: str, port: int, user: str, password: str, database: str, **kwargs):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    return conn

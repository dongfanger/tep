from tep import pymysql

from data.GlobalData import GlobalData


def test():
    sql = 'select 1 from dual'
    rows = pymysql(GlobalData.db, sql)
    for row in rows:
        print(row['1'])


def test_null():
    sql = 'select 1 from dual where 1 = 0'
    rows = pymysql(GlobalData.db, sql)
    if not rows:
        pass
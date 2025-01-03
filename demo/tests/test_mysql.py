from tep import pymysql

from data.global_data import GlobalData


def test():
    sql = "select 1 from dual"
    rows = pymysql(GlobalData.db, sql)
    for row in rows:
        print(row["1"])

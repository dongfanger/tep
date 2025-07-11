#!/usr/bin/python
# encoding=utf-8

import pymysql

from tep.patch.patch_logging import logger


def patch_pymysql(db: dict, sql: str):
    """
    Return type: list | None
    """
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], password=db['password'], database=db['database'])
        cursor = conn.cursor()
        _execute(cursor, sql)
        conn.commit()
        return _rows(cursor)
    except Exception as e:
        logger.error(f'Database execute error, {e}')
        conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def _execute(cursor, sql):
    seq = ';'
    if seq in sql:
        for s in sql.split(seq):
            s = s.strip().strip('\\n')
            if s:
                cursor.execute(s)
    else:
        if sql:
            cursor.execute(sql)


def _rows(cursor):
    rows = cursor.fetchall()
    if not rows:
        return None

    names = [desc[0] for desc in cursor.description]
    # Get row by name
    # rows [{'a': 1, 'b': 1}, {'a': 2, 'b': 2}]
    # row {'a': 1, 'b': 1}
    return [{name: row[names.index(name)] for name in names} for row in rows]

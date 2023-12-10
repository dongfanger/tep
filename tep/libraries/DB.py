from loguru import logger


class DB:
    @classmethod
    def pymysql_execute(cls, conn, cursor, sql):
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logger.error(f"Database execute error: {e}")
            conn.rollback()

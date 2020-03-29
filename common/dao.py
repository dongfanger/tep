#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   : 2020/3/17 14:30
@Desc   : Database access object
"""

import pandas as pd
from pymysql import InternalError
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from texttable import Texttable

from common.pytest_logger import logger


class Dao:
    def __init__(self, address, user, password):
        """Initial

        @param address: Host:port/database
        @param user: User for database
        @param password: Password for database
        """
        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{address}')
        self.data_frame = None
        pd.set_option('display.max_columns', 100)
        pd.set_option('display.width', 2000)

    def select(self, sql):
        """Select statement

        :param sql: Sql to run
        :return: DataFrame. how to get? data['col_name']['row_index'] eg:data['id'][0]
        """
        logger.info(f'Running sql\n{sql}')
        try:
            self.data_frame = pd.read_sql(sql, self.engine)
        except (InternalError, ProgrammingError):
            logger.info(f"{'*' * 26}\n"
                        f"Sql error\n"
                        f"{'*' * 26}\n")
            assert False

        tb = Texttable()
        tb.header(self.data_frame.columns.array)
        tb.set_max_width(0)
        # Set data type 't', total text * cols
        tb.set_cols_dtype(['t'] * self.data_frame.shape[1])
        tb.add_rows(self.data_frame.to_numpy(), header=False)
        logger.info(f'Sql result:\n{tb.draw()}')
        return self._convert_data_type()

    def _convert_data_type(self):
        """Convert data type

        @return: Converted data
        """
        columns = self.data_frame.columns
        data = {k: list(self.data_frame[k]) for k in columns}
        data = {k: [self._convert(x) for x in v] for k, v in data.items()}
        return data

    @staticmethod
    def _convert(x):
        """Convert logic code

        @param x: Single cell data
        @return: Converted single cell data
        """
        # float to int
        if isinstance(x, float) and x % 1 == 0:
            return int(x)
        return x


def test():
    Dao('localhost:3306/new_schema', 'root', '123456').select('select * from new_table;')

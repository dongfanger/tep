#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  9/2/2020 11:32 AM
@Desc    :  
"""

from loguru import logger

try:
    from sqlalchemy import create_engine
    from texttable import Texttable
except ModuleNotFoundError:
    pass


def mysql_engine(host, port, user, password, db):
    try:
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
    except NameError:
        return ""
    return engine


def print_db_table(data_frame):
    tb = Texttable()
    tb.header(data_frame.columns.array)
    tb.set_max_width(0)
    # text * cols
    tb.set_cols_dtype(['t'] * data_frame.shape[1])
    tb.add_rows(data_frame.to_numpy(), header=False)
    logger.info(tb.draw())

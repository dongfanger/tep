#!/usr/bin/python
# encoding=utf-8
from loguru import logger


def test_mysql(pd, env_vars):
    logger.info(pd.read_sql("select 1 from dual", env_vars.mysql_engine))

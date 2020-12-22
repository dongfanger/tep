#!/usr/bin/python
# encoding=utf-8

from loguru import logger


def test_login(login, pd, env_vars):
    logger.info(login.token)
    logger.info(pd.read_sql("select 1 from dual", env_vars.mysql_engine))

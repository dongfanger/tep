#!/usr/bin/python
# encoding=utf-8

from loguru import logger


def test_login(login):
    logger.info(login.token)

#!/usr/bin/python
# encoding=utf-8

"""
@Author : dongfanger
@Date   : 2019/12/12 10:58
@Desc   : console handler will be created by pytest, here is just file handler
"""

import logging
import sys

from config.relative_path import log_file

logger = logging.getLogger()
# default WARN
logger.setLevel(logging.INFO)
_formatter = logging.Formatter('[%(asctime)s]%(message)s', '%Y-%m-%d %H:%M:%S')
_stdout = sys.stdout
if all('FileHandler' not in str(handler) for handler in logger.handlers):
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(_formatter)
    logger.addHandler(file_handler)


def stdout_write(msg):
    """for processing bar

    @param msg: message
    """
    _stdout.write(msg)
    _stdout.flush()


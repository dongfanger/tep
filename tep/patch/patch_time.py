#!/usr/bin/python
# encoding=utf-8
import inspect
import time

from tep.patch.patch_logging import logger


def patch_time(f='%Y-%m-%d'):
    return time.strftime(f, time.localtime(time.time()))


def timestamp(specified_time=None):
    if specified_time:
        try:
            return int(time.mktime(time.strptime(specified_time, '%Y-%m-%d %H:%M:%S')) * 1000)  # ms
        except ValueError:
            caller_code = inspect.currentframe().f_back.f_code
            logger.error(f'{caller_code.co_filename}::{caller_code.co_name} error, YYYY-MM-DD HH:MM:SS, return -1')
            return -1

    return int(time.time() * 1000)  # ms

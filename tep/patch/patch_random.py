#!/usr/bin/python
# encoding=utf-8
import inspect
import random
from tep.patch.patch_logging import logger


def patch_random(*args, **kwargs):
    try:
        if len(args) == 0:
            return _get_random_num(8)
        if len(args) == 1:
            return _get_random_num(int(args[0]))
        if len(args) == 2:
            return str(args[0]) + str(_get_random_num(int(args[1])))
    except:
        caller_code = inspect.currentframe().f_back.f_code
        logger.error(f'{caller_code.co_filename}::{caller_code.co_name} error, return -1')
        return -1


def _get_random_num(n):
    lower_bound = 10 ** (n - 1)
    upper_bound = 10 ** n - 1
    return random.randint(lower_bound, upper_bound)

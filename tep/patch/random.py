#!/usr/bin/python
# encoding=utf-8
import inspect
import logging
import random as rnd


def random(*args, **kwargs):
    try:
        if len(args) == 0:
            return _get_random_num(8)

        if len(args) == 1:
            return _get_random_num(int(args[0]))

        if len(args) == 2:
            return str(args[0]) + str(_get_random_num(int(args[1])))
    except:
        caller_code = inspect.currentframe().f_back.f_code
        logging.error(f"{caller_code.co_filename}::{caller_code.co_name} error, return -1")
        return -1


def _get_random_num(n):
    lower_bound = 10 ** (n - 1)
    upper_bound = 10 ** n - 1
    return rnd.randint(lower_bound, upper_bound)
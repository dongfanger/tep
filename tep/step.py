#!/usr/bin/python
# encoding=utf-8

from tep.patch.patch_logging import logger


def step(name: str, function):
    logger.info('----------------' + name + '----------------')
    return function()

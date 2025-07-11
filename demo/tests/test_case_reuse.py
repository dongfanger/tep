#!/usr/bin/python
# encoding=utf-8

from tep import v, step, logger


def test(case_hello):
    v({
        "name": "Gang"
    })
    case_hello()
    step('welcome', step_welcome)


def step_welcome():
    logger.info('Welcome to tep')

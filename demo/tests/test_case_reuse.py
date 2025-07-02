#!/usr/bin/python
# encoding=utf-8

from tep import v, step


def test(case_hello):
    v({
        "name": "Gang"
    })
    case_hello()
    step('welcome', step_welcome)


def step_welcome():
    print('Welcome to tep')

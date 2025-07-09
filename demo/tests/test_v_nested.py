#!/usr/bin/python
# encoding=utf-8
from tep import v


def test():
    v({
        "welcome": "${msg}, welcome to tep",
        "msg": "Hello ${name}",
        "name": "Gang"
    })
    print(v('welcome'))
    x = '${welcome}, Never too late to learn.'
    print(v(x))

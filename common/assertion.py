#!/usr/bin/python
# encoding=utf-8

"""
@Author : dongfanger
@Date   : 2019/12/12 10:58
@Desc   : assertions
"""


def status_ok(r):
    """response status is ok

    @param r: response object
    """
    assert r.status_code < 400

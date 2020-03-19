#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   : 2019/12/12 10:58
@Desc   : Assertions
"""


def status_ok(r):
    """Response status is ok

    @param r: Response object
    """
    assert r.status_code < 400

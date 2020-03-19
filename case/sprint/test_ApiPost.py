#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   :  2020-03-19 12:14:22
@Desc   : 
"""

from api.bu.ApiPost import ApiPost
from data.env import vars_


def test_default():
    x = ApiPost()
    x.load().send()

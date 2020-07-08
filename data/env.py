#!/usr/bin/python
# encoding=utf-8

"""
@Author : dongfanger
@Date   : 2020/2/20 10:36
@Desc   : user defined variables by different environment
"""

import uuid

from common.dao import Dao


class Dev:
    test_url = 'https://x'
    headers = {"Content-Type": "application/json"}
    # dao_x = Dao('host:port',
    #             'username',
    #             'password')


class Qa:
    test_url = 'http://www.mockhttp.cn'
    headers = {"Content-Type": "application/json"}
    # dao_x = Dao('host:port',
    #             "username",
    #             "password")


def uuid_list(n):
    """uuid list

    @param n: number
    @return: A uuid list
    """
    return [str(uuid.uuid4()).replace('-', '') for i in range(n)]

#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   : 2020/2/20 10:36
@Desc   : User defined variables by different environment
"""

import uuid

from common.dao import Dao


class _GldExp:
    x = 1
    headers = {"Content-Type": "application/json"}
    dao_x = Dao('host:port',
                'username',
                'password')

    test_url = 'https://x'


class _Gld:
    x = 2
    headers = {"Content-Type": "application/json"}
    dao_x = Dao('host:port',
                "username",
                "password")

    test_url = 'https://x'


def uuid_list(n):
    """Uuid list

    @param n: Number
    @return: A uuid list
    """
    return [str(uuid.uuid4()).replace('-', '') for i in range(n)]


# Set environment name
vars_ = _GldExp

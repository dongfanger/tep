#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   : 2020/2/17 17:06
@Desc   : Base api class
"""

from common.assertion import status_ok
from common.pytest_logger import logger
from common.request import Request


class Api:
    def __init__(self):
        self.url = None
        self.body = None
        self.req = Request()
        self.res = None
        self.content = {}

    def set_content(self):
        """After request, assert status and set content

        """
        status_ok(self.res)
        res_json = self.res.json()
        assert 1000 == res_json.get('status')
        try:
            self.content = res_json['content']
        except KeyError:
            logger.info(f"{'*' * 26}\n"
                        f"Response no content\n"
                        f"{'*' * 26}\n")

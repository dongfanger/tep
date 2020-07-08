#!/usr/bin/python
# encoding=utf-8

"""
@Author : dongfanger
@Date   : 2020/2/17 17:06
@Desc   : base api
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

    def assert_response_status(self):
        """after request, assert response status and set content

        """
        # http status
        status_ok(self.res)
        res_json = self.res.json()
        # business status
        assert res_json.get('status') == 1000
        try:
            self.content = res_json['content']
        except KeyError:
            logger.info(f"\n{'*' * 26}\n"
                        f"response no content\n"
                        f"{'*' * 26}\n")

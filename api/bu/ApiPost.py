#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   :  2020-03-19 12:14:22
@Desc   :  Demo auto code
"""

from api.base import Api
from data.env import vars_


class ApiPost(Api):

    def __init__(self):
        super().__init__()
        self.url = vars_.test_url + "/api/post"

    def load(self):
        self.body = {}

        return self

    def send(self):
        self.res = self.req.post(url=self.url, headers=vars_.headers, json=self.body)
        self.set_content()
        return self.res

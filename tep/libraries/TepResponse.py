#!/usr/bin/python
# encoding=utf-8

import jsonpath
from requests import Response


class TepResponse(Response):
    """
    Inherit on requests.Response, adding additional methods
    """

    def __init__(self, response):
        super().__init__()
        for k, v in response.__dict__.items():
            self.__dict__[k] = v

    def jsonpath(self, expr: str):
        """
        Force the first value here for simple values
        If complex values are taken, it is recommended to use jsonpath native directly
        """
        return jsonpath.jsonpath(self.json(), expr)[0]

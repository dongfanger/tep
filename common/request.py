#!/usr/bin/python
# encoding=utf-8

"""
@Author : dongfanger
@Date   : 2019/12/12 10:58
@Desc   : packaging requests lib
"""

import decimal
import json
import time

import requests
import urllib3
from requests.api import request

from common.func import current_time, NpEncoder, report_csv
from common.pytest_logger import logger
from pytest_allure import api_log_level
from config.relative_path import interface_called_info_file

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def method(f):
    """decorator

    @param f: decorated function
    @return: inner function
    """

    def send(self, *args, **kwargs):
        self.param["method"] = f.__name__
        if api_log_level in (1, 3):
            logger.info(f"requesting")
            for k, v in kwargs.items():
                try:
                    if isinstance(v, dict):
                        v = json.dumps(v, ensure_ascii=False, cls=NpEncoder)
                        kwargs[k] = json.loads(v)
                except TypeError:
                    logger.info(f"{'>' * 16}\n"
                                f"parameterize failed, probable cause:\n"
                                f"no double quote\n"
                                f"get sql data not by index\n"
                                f"{'<' * 16}\n")
                # url headers json/data
                logger.info(f"""{k}\n{str(v).replace("'", '"')}""")
        start = time.process_time()
        while True:
            try:
                self.param['r'] = f(self, *args, **kwargs)
            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                if 'bad handshake' in str(e) or '10054' in str(e):
                    logger.info(f"{'>' * 16}read time out, retrying{'<' * 16}")
                    continue
                else:
                    raise Exception(e)
            break
        end = time.process_time()

        self.param['elapsed'] = decimal.Decimal("%.2f" % float(end - start))
        self._response_log(*args, **kwargs)
        return self.param['r']

    return send


class Request:
    def __init__(self):
        self.param = {
            "default_headers": {"Content-Type": "application/json"},
            "p": None,
            "method": None,
            "r": None,
            "elapsed": None
        }

    def _response_log(self, *args, **kwargs):
        """response log info

        @param args: list args
        @param kwargs: keyword args
        """
        param = self.param
        if api_log_level in (1, 3):
            try:
                logger.info(f"response\n{param['r'].text}")
            except AttributeError:
                logger.info(f"{'>' * 16}\n"
                            f"request failed\n"
                            f"{'<' * 16}\n")

        if api_log_level in (2, 3):
            title = ['time', 'status', 'elapsed(s)', 'request', 'response']
            row = [current_time(),
                   param['r'].status_code,
                   param['elapsed'],
                   f"{args}{json.dumps(kwargs, ensure_ascii=False)}",
                   param['r'].text,
                   ' ']
            report_csv(interface_called_info_file, title, row)

    @method
    def get(self, url, params=None, **kwargs):
        r"""Sends a GET request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', True)
        return request('get', url, params=params, **kwargs)

    @method
    def options(self, url, **kwargs):
        r"""Sends an OPTIONS request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', True)
        return request('options', url, **kwargs)

    @method
    def head(self, url, **kwargs):
        r"""Sends a HEAD request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', False)
        return request('head', url, **kwargs)

    @method
    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return request('post', url, data=data, json=json, **kwargs)

    @method
    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return request('put', url, data=data, **kwargs)

    @method
    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return request('patch', url, data=data, **kwargs)

    @method
    def delete(self, url, **kwargs):
        r"""Sends a DELETE request.

        :param url: URL for the new :class:`Request` object.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return request('delete', url, **kwargs)

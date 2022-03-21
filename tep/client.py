#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  7/25/2020 2:02 PM
@Desc    :  轻度封装requests库
"""

import decimal
import json
import time

import allure
import jmespath
import requests
import urllib3
from loguru import logger
from requests import sessions, Response

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def tep_request_monkey_patch(req, *args, **kwargs):
    start = time.process_time()
    response = req(*args, **kwargs)
    end = time.process_time()
    elapsed = str(decimal.Decimal("%.3f" % float(end - start))) + "s"
    log4a = "{}{} status:{}  response:{}  elapsed:{}"
    try:
        kv = ""
        for k, v in kwargs.items():
            # if not json, str()
            try:
                v = json.dumps(v, ensure_ascii=False)
            except TypeError:
                v = str(v)
            kv += f" {k}:{v} "
        args = list(args)
        args += ["", ""]
        method, url, *t = args
        method_url = ""
        if method:
            method_url = f'method:"{method}" '
        if url:
            method_url += f'\nurl:"{url}" '
        request_response = log4a.format(method_url, kv, response.status_code, response.text, elapsed)
        logger.info(request_response)
        allure.attach(request_response, f'request & response', allure.attachment_type.TEXT)
    except AttributeError:
        logger.error("request failed")
    except TypeError:
        logger.warning(log4a)
    return response


def request_wrapper(req):
    def send(*args, **kwargs):
        return tep_request_monkey_patch(req, *args, **kwargs)

    return send


@request_wrapper
def request(method, url, **kwargs):  # 从requests库原样拷贝而来
    """Constructs and sends a :class:`Request <Request>`.

    :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Usage::

      >>> import requests
      >>> req = requests.request('GET', 'https://httpbin.org/get')
      >>> req
      <Response [200]>
    """

    # By using the 'with' statement we are sure the session is closed, thus we
    # avoid leaving sockets open which can trigger a ResourceWarning in some
    # cases, and look like a memory leak in others.
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)


class TepResponse(Response):
    def __init__(self, response):
        super().__init__()
        for k, v in response.__dict__.items():
            self.__dict__[k] = v

    def jmespath(self, expression):
        return jmespath.search(expression, self.json())


class BaseRequest:
    def __init__(self, clazz):
        self.case_vars = clazz.case_vars

    def request(self, method, url, **kwargs):
        response = request(method, url, **kwargs)
        return TepResponse(response)

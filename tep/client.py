#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  7/25/2020 2:02 PM
@Desc    :
"""

import decimal
import json
import time

import requests
import urllib3
from loguru import logger
from requests import sessions

from tep.funcs import NpEncoder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def request_encapsulate(req):
    def send(*args, **kwargs):
        start = time.process_time()
        response = req(*args, **kwargs)
        end = time.process_time()
        elapsed = str(decimal.Decimal("%.3f" % float(end - start))) + "s"

        # log
        try:
            log4a = {"method": args[0]}
            for k, v in kwargs.items():
                # if not json, str()
                try:
                    json.dumps(v)
                except TypeError:
                    v = str(v)
                log4a.setdefault(k, v)
            log4a.setdefault("status", response.status_code)
            log4a.setdefault("response", response.text)
            log4a.setdefault("elapsed", elapsed)
            logger.info(json.dumps(log4a, ensure_ascii=False, cls=NpEncoder))
        except AttributeError:
            logger.error("request failed")
        except TypeError:
            logger.warning(log4a)

        return response

    return send


@request_encapsulate
def request(method, url, **kwargs):
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

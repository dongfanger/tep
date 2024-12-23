#!/usr/bin/python
# encoding=utf-8

import json
import logging
from urllib.parse import unquote

import httpx
import jsonpath
import requests
import urllib3
from requests import Response

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TepResponse(Response):
    """
    Inherit on requests.Response, adding additional methods
    """

    def __init__(self, response):
        super().__init__()
        for k, v in response.__dict__.items():
            self.__dict__[k] = v

    def jsonpath(self, expr: str):
        return jsonpath.jsonpath(self.json(), expr)


_template = """\n
URL: {url}
Method: {method}
Headers: {headers}
Request Body: {request_body}
Status Code: {status_code}
Response Body: {response_body}
Elapsed: {elapsed}ms
"""


def request(method, url, **kwargs):
    http2 = kwargs.pop("http2", False)
    if http2:
        return _http2(method, url, **kwargs)
    return _http1(method, url, **kwargs)


def _http1(method, url, **kwargs):
    response = requests.request(
        method, url,
        hooks={'response': _response_callback},
        **kwargs
    )
    return TepResponse(response)


def _http2(method, url, **kwargs):
    with httpx.Client(event_hooks={'response': [_response2_callback]}) as client:
        r = client.request(method, url, **kwargs)
        return r


def _response_callback(response, *args, **kwargs):
    log = _template.format(
        url=unquote(response.request.url),
        method=response.request.method,
        headers=_json_str(response.request.headers),
        request_body=_json_str(response.request.body),
        status_code=response.status_code,
        response_body=response.text,
        elapsed=round(response.elapsed.total_seconds() * 1000, 2)
    )
    logging.info(log)


def _response2_callback(response: httpx.Response):
    response.read()
    log = _template.format(
        url=response.request.url,
        method=response.request.method,
        headers=_json_str(response.request.headers),
        request_body=_json_str(response.request.content),
        status_code=response.status_code,
        response_body=response.text,
        elapsed=response.elapsed.total_seconds()
    )
    logging.info(log)


def _json_str(o):
    if not o:
        return o

    try:
        return json.dumps(o, ensure_ascii=False)
    except:
        pass

    try:
        return json.dumps(json.loads(o.decode("utf-8")), ensure_ascii=False)  # bytes
    except:
        pass

    try:
        return json.dumps(dict(o), ensure_ascii=False)  # requests.structures.CaseInsensitiveDict
    except:
        pass

    return o

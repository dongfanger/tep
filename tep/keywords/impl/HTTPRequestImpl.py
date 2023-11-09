#!/usr/bin/python
# encoding=utf-8

import json
from typing import Any
from urllib.parse import unquote

import requests
import urllib3
from loguru import logger
from requests.structures import CaseInsensitiveDict

from tep.libraries.Result import Result
from tep.libraries.TepResponse import TepResponse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_template = """\n
        URL: {url}
        Method: {method}
        Headers: {headers}
        Request Body: {request_body}
        Status Code: {status_code}
        Response Body: {response_body}
        Elapsed: {elapsed}s
        """


def HTTPRequestImpl(method, url, **kwargs) -> Result:
    """
    Requests.request native usage, adding response callbacks
    """
    response = requests.request(
        method, url,
        hooks={'response': _response_callback},
        **kwargs
    )
    result = Result()
    result.response = TepResponse(response)
    return result


def _response_callback(response, *args, **kwargs):
    """
    Response callback, recording request meta information
    """
    log = _template.format(
        url=unquote(response.request.url),
        method=response.request.method,
        headers=_json_text(response.request.headers),
        request_body=_json_text(response.request.body),
        status_code=response.status_code,
        response_body=response.text,
        elapsed=response.elapsed.total_seconds()
    )
    logger.info(log)


def _json_text(o: Any) -> [str, Any]:
    try:
        if not o:
            return o
        elif isinstance(o, bytes):
            return json.dumps(json.loads(o.decode("utf-8")), ensure_ascii=False)
        elif isinstance(o, dict) or isinstance(o, list) or isinstance(o, str):
            return json.dumps(o, ensure_ascii=False)
        elif isinstance(o, CaseInsensitiveDict):
            return json.dumps(dict(o), ensure_ascii=False)
        else:
            logger.warning("JSON parse unknown type: {}", type(o))
            return o
    except Exception as e:
        logger.error("JSON parse exception: {}", e)
        return o

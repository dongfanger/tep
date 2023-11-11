from httpx import Response
from loguru import logger

from tep.libraries.TepResponse import TepResponse


def test(HTTPRequestKeyword):
    logger.info("run request with HTTP/1.1 and HTTP/2")
    ctx = {"baseUrl": "https://postman-echo.com"}

    logger.info("HTTP/1.1 get")
    body = {"foo1": "foo1", "foo2": "foo2"}
    ro = HTTPRequestKeyword("get", url=ctx["baseUrl"] + "/get", headers={"User-Agent": "tep"}, params=body)
    response: TepResponse = ro.response
    assert response.status_code == 200
    assert len(body["foo1"]) == 4

    logger.info("HTTP/1.1 post")
    body = {"foo1": "foo1", "foo2": "foo2"}
    ro = HTTPRequestKeyword("post", url=ctx["baseUrl"] + "/post", headers={"User-Agent": "tep"}, params=body)
    response: TepResponse = ro.response
    assert response.status_code == 200
    assert len(body["foo1"]) == 4

    logger.info("HTTP/2 get")
    body = {"foo1": "foo1", "foo2": "foo2"}
    ro = HTTPRequestKeyword("get", url=ctx["baseUrl"] + "/get", headers={"User-Agent": "tep"}, params=body, http2=True)
    response: Response = ro.response
    assert response.status_code == 200
    assert len(body["foo1"]) == 4

    logger.info("HTTP/2 post")
    body = {"foo1": "foo1", "foo2": "foo2"}
    ro = HTTPRequestKeyword("post", url=ctx["baseUrl"] + "/post", headers={"User-Agent": "tep"}, params=body, http2=True)
    response: Response = ro.response
    assert response.status_code == 200
    assert len(body["foo1"]) == 4

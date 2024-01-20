import logging

def test(HTTPRequestKeyword):
    logging.info("run request with HTTP/1.1 and HTTP/2")
    ctx = {"baseUrl": "https://postman-echo.com"}

    logging.info("HTTP/1.1 get")
    body = {"foo1": "foo1", "foo2": "foo2"}
    response = HTTPRequestKeyword("get", url=ctx["baseUrl"] + "/get", headers={"User-Agent": "tep"}, params=body)
    assert response.status_code == 200
    assert len(body["foo1"]) == 4

    logging.info("HTTP/1.1 post")
    body = {"foo1": "foo1", "foo2": "foo2"}
    response = HTTPRequestKeyword("post", url=ctx["baseUrl"] + "/post", headers={"User-Agent": "tep"}, params=body)
    assert response.status_code == 200
    assert len(body["foo1"]) == 4

    logging.info("HTTP/2 get")
    body = {"foo1": "foo1", "foo2": "foo2"}
    response = HTTPRequestKeyword("get", url=ctx["baseUrl"] + "/get", headers={"User-Agent": "tep"}, params=body, http2=True)
    assert response.status_code == 200
    assert len(body["foo1"]) == 4

    logging.info("HTTP/2 post")
    body = {"foo1": "foo1", "foo2": "foo2"}
    response = HTTPRequestKeyword("post", url=ctx["baseUrl"] + "/post", headers={"User-Agent": "tep"}, params=body, http2=True)
    assert response.status_code == 200
    assert len(body["foo1"]) == 4

def test(HTTPRequestKeyword):
    ro = HTTPRequestKeyword("get", url="http://httpbin.org/status/200")
    assert ro.response.status_code == 200

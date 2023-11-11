def test(HTTPRequestKeyword):
    ro = HTTPRequestKeyword("get", url="http://httpbin.org/status/200", http2=True)
    assert ro.response.status_code == 200

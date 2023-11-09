from tep.libraries.TepResponse import TepResponse


def test(HTTPRequestKeyword):
    ro = HTTPRequestKeyword("get", url="http://httpbin.org/status/200")
    response: TepResponse = ro.response
    assert response.status_code == 200

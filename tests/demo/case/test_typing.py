from tep.libraries.TepResponse import TepResponse


def test(HTTPRequestKeyword):
    response: TepResponse = HTTPRequestKeyword("get", url="http://httpbin.org/status/200")
    assert response.status_code == 200

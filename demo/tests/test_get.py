from tep import request


def test():
    response = request("get", url="http://httpbin.org/status/200")
    assert response.status_code == 200

import pytest

from tep.libraries.Result import Result


@pytest.fixture(scope="session")
def login(HTTPRequestKeyword):
    def _function() -> Result:
        url = "http://127.0.0.1:5000/login"
        headers = {"Content-Type": "application/json"}
        body = {"username": "dongfanger", "password": "123456"}
        ro = HTTPRequestKeyword("post", url=url, headers=headers, json=body)
        response = ro.response
        assert response.status_code < 400
        ro = Result()
        ro.data = {"Content-Type": "application/json", "Cookie": f"{response.json()['Cookie']}"}
        return ro

    return _function

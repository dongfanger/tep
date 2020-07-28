import pytest
from faker import Faker


def json_token_headers(token):
    return {"Content-Type": "application/json", "token": token}


headers = {"Content-Type": "application/json"}
fake = Faker(locale='zh_CN')


class Dev:
    test_url = 'https://dev.com'
    # dao_x = Dao('host:port',
    #             'username',
    #             'password')


class Qa:
    test_url = 'https://qa.com'
    # dao_x = Dao('host:port',
    #             "username",
    #             "password")


class Release:
    test_url = 'https://release.com'
    # dao_x = Dao('host:port',
    #             "username",
    #             "password")


# choose environment
env = Release


@pytest.fixture()
def admin_login_token():
    token = 'test_token'
    return token

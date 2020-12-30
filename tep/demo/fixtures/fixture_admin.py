#!/usr/bin/python
# encoding=utf-8

""" Can only be modified by the administrator. Only fixtures are provided.
"""

import jmespath

from tep.client import request
from tep.dao import mysql_engine
from tep.fixture import *


@pytest.fixture(scope="session")
def env_vars(config):
    class Clazz(EnvVars):
        def __init__(self):
            super().__init__()
            self.env = config["env"]

            # Preset environment and variables
            self.mapping = {
                "qa": {
                    "domain": "https://qa.com",
                    "mysql_engine": mysql_engine("127.0.0.1",  # host
                                                 "2306",  # port
                                                 "root",  # username
                                                 "123456",  # password
                                                 "test"),  # db_name
                },
                "release": {
                    "domain": "https://release.com",
                    "mysql_engine": mysql_engine("127.0.0.1",
                                                 "2306",
                                                 "root",
                                                 "123456",
                                                 "release"),
                }
                # Add your environment and variables
            }
            self.domain = self.mapping[self.env]["domain"]
            self.mysql_engine = self.mapping[self.env]["mysql_engine"]
            # Add properties

    return Clazz()


def _jwt_headers(token):
    return {"Content-Type": "application/json", "authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def login(url):
    # Code your login
    logger.info("Administrator login")
    response = request(
        "post",
        url=url("/api/users/login"),
        headers={"Content-Type": "application/json"},
        json={
            "username": "admin",
            "password": "123456",
        }
    )
    assert response.status_code < 400
    response_token = jmespath.search("token", response.json())

    class Clazz:
        token = response_token
        jwt_headers = _jwt_headers(response_token)

    return Clazz

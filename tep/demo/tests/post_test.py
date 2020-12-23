#!/usr/bin/python
# encoding=utf-8
import jmespath
from loguru import logger

from tep.client import request


def test_post(faker_ch, url, login):
    # description
    logger.info("test post")
    # data
    fake = faker_ch
    # request
    response = request(
        "post",
        url=url("/api/users"),
        headers=login.jwt_headers,
        json={
            "name": fake.name()
        }
    )
    # assert
    assert response.status_code < 400
    # extract
    user_id = jmespath.search("id", response.json())

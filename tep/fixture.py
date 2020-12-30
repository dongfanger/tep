#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2020/12/30 9:30
@Desc    :  
"""
import os

import pytest
import yaml
from faker import Faker
from loguru import logger


class Project:
    dir = ""


def pytest_sessionstart(session):
    Project.dir = session.config.cache.get("project_dir", None)


@pytest.fixture(scope="session")
def url(env_vars):
    def domain_and_uri(uri):
        if not uri.startswith("/"):
            uri = "/" + uri
        return env_vars.domain + uri

    return domain_and_uri


@pytest.fixture(scope="session")
def faker_ch():
    return Faker(locale="zh_CN")


@pytest.fixture(scope="session")
def faker_en():
    return Faker()


@pytest.fixture(scope="session")
def pd():
    import pandas
    return pandas


@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(Project.dir, "conf.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        conf = yaml.load(f.read(), Loader=yaml.FullLoader)
        return conf


@pytest.fixture(scope="session")
def files_dir():
    return os.path.join(Project.dir, "files")


class EnvVars:
    def __init__(self):
        self.env = ""
        self.mapping = {}

    def put(self, key, value):
        self.mapping[self.env][key] = value

    def get(self, key):
        value = ""
        try:
            value = self.mapping[self.env][key]
        except KeyError:
            logger.error(f"env_vars doesnt have this key: {key}")
        return value

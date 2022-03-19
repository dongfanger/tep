#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2020/12/30 9:30
@Desc    :  Provide some fixtures
"""

import os

import jmespath
import pytest
import yaml
from faker import Faker
from loguru import logger


class Project:
    dir = ""


def _project_dir(session):
    project_dir = session.config.cache.get("project_dir", None)
    if not project_dir:
        cwd = os.getcwd()
        tests = cwd.find("tests")
        samples = cwd.find("samples")
        if tests > 0:
            project_dir = cwd[:cwd.find("tests")]
        elif samples > 0:
            project_dir = cwd[:cwd.find("samples")]
        else:
            project_dir = cwd
    return project_dir


def pytest_sessionstart(session):
    Project.dir = _project_dir(session)


@pytest.fixture(scope="session")
def faker_ch():
    return Faker(locale="zh_CN")


@pytest.fixture(scope="session")
def faker_en():
    return Faker()


@pytest.fixture(scope="session")
def pd():
    try:
        import pandas
        return pandas
    except ModuleNotFoundError:
        pass


@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(Project.dir, "conf.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        conf = yaml.load(f.read(), Loader=yaml.FullLoader)
        return conf


@pytest.fixture(scope="session")
def files_dir():
    return os.path.join(Project.dir, "files")


class TepVars:
    def __init__(self):
        self.vars_ = {}

    def put(self, key, value):
        self.vars_[key] = value

    def get(self, key):
        value = ""
        try:
            value = self.vars_[key]
        except KeyError:
            logger.error(f"env_vars doesnt have this key: {key}")
        return value


_jmespath_import_placeholder = jmespath.search("abc", "abc")

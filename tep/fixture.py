#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2020/12/30 9:30
@Desc    :  预置fixture
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
    # 从缓存中获取项目根目录
    project_dir = session.config.cache.get("project_dir", None)
    if not project_dir:
        # 第一次运行没有.pytest_cache
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
    """中文造数据"""
    return Faker(locale="zh_CN")


@pytest.fixture(scope="session")
def faker_en():
    """英文造数据"""
    return Faker()


@pytest.fixture(scope="session")
def pd():
    """pandas库"""
    try:
        import pandas
        return pandas
    except ModuleNotFoundError:
        pass


@pytest.fixture(scope="session")
def config():
    """读取conf.yaml配置文件"""
    config_path = os.path.join(Project.dir, "conf.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        conf = yaml.load(f.read(), Loader=yaml.FullLoader)
        return conf


@pytest.fixture(scope="session")
def files_dir():
    """files目录的路径"""
    return os.path.join(Project.dir, "files")


class TepVars:
    """全局变量池"""

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


# 预先import某些包，fixtures/下脚本只需要from tep.fixture import *即可
# 无实际意义
_nothing = jmespath.search("abc", "abc")

#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  dongfanger
@Date    :  2020/12/30 9:30
@Desc    :  预置fixture
"""
import json
import os

import pytest
import yaml
from filelock import FileLock
from loguru import logger

from tep.config import tep_config, Config


class TepVars:
    """
    动态变量池
    """

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


@pytest.fixture(scope="session")
def env_vars():
    """
    环境变量，读取resources/env_vars下的变量模板，返回字典
    """

    class Clazz(TepVars):
        def dict_(self):
            env_active = tep_config()['env']["active"]
            env_filename = f"env_vars_{env_active}.yaml"
            with open(
                    os.path.join(Config.project_root_dir, "resources", "env_vars", env_filename)) as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)

    return Clazz().dict_()


@pytest.fixture(scope="session")
def global_vars():
    """
    全局变量，读取resources/global_vars.yaml，返回字典
    """

    class Clazz(TepVars):
        def dict_(self):
            with open(os.path.join(Config.project_root_dir, "resources", "global_vars.yaml")) as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)

    return Clazz().dict_()


@pytest.fixture(scope="session")
def tep_context_manager(tmp_path_factory, worker_id):
    """
    tep上下文管理器，在xdist分布式执行时，仅初始化一次
    参考：https://pytest-xdist.readthedocs.io/en/latest/how-to.html#making-session-scoped-fixtures-execute-only-once
    命令不带-n auto也能正常执行，不受影响
    """

    def inner(produce_expensive_data, *args, **kwargs):
        if worker_id == "master":
            # not executing in with multiple workers, just produce the data and let
            # pytest's fixture caching do its job
            return produce_expensive_data(*args, **kwargs)

        # get the temp directory shared by all workers
        root_tmp_dir = tmp_path_factory.getbasetemp().parent

        fn = root_tmp_dir / "data.json"
        with FileLock(str(fn) + ".lock"):
            if fn.is_file():
                data = json.loads(fn.read_text())
            else:
                data = produce_expensive_data(*args, **kwargs)
                fn.write_text(json.dumps(data))
        return data

    return inner

#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  dongfanger
@Date    :  2020/12/30 9:30
@Desc    :  预置fixture
"""
import os

import pytest
import yaml
from loguru import logger

from tep.config import tep_config, Config


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


@pytest.fixture(scope="session")
def env_vars():
    """环境变量，读取resources/env_vars下的变量模板"""
    class Clazz(TepVars):
        def dict_(self):
            env_active = tep_config()['env']["active"]
            env_filename = f"env_vars_{env_active}.yaml"
            with open(
                    os.path.join(Config.project_root_dir, "resources", "env_vars", env_filename)) as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)

    return Clazz().dict_()

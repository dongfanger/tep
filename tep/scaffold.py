#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  7/23/2020 8:12 PM
@Desc    :
"""

import os
import sys

from loguru import logger


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser(
        "startproject", help="Create a new project with template structure."
    )
    sub_parser_scaffold.add_argument(
        "project_name", type=str, nargs="?", help="Specify new project name."
    )
    return sub_parser_scaffold


def create_scaffold(project_name):
    """ Create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        logger.warning(
            f"Project folder {project_name} exists, please specify a new project name."
        )
        return 1
    elif os.path.isfile(project_name):
        logger.warning(
            f"Project name {project_name} conflicts with existed file, please specify a new one."
        )
        return 1

    logger.info(f"Create new project: {project_name}")
    print(f"Project root dir: {os.path.join(os.getcwd(), project_name)}\n")

    def create_folder(path):
        os.makedirs(path)
        msg = f"Created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"Created file: {path}"
        print(msg)

    git_ignore = "\n".join(
        [".idea/", ".pytest_cache/", ".tep_allure_tmp/", "__pycache__/", "*.pyc", "reports/", "debug/"]
    )

    conf_yaml = """env: qa"""

    conftest = """#!/usr/bin/python
# encoding=utf-8
\"\"\" Can only be modified by the administrator. Only fixtures are provided.
\"\"\"


import os

import pytest
import yaml

# Initial
_project_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session", autouse=True)
def project_cache(request):
    request.config.cache.set("project_dir", _project_dir)


@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(_project_dir, "conf.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        conf = yaml.load(f.read(), Loader=yaml.FullLoader)
        return conf


@pytest.fixture(scope="session")
def files_dir():
    return os.path.join(_project_dir, "files")


# Import fixtures
exec("from fixtures.fixture_admin import *")
exec("from fixtures.fixture_don import *")
"""

    pytest_ini = """[pytest]
markers =
    smoke: 冒烟测试
    regress: 回归测试
"""

    fixture_admin = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Can only be modified by the administrator. Only fixtures are provided.
\"\"\"

import pytest
from faker import Faker
from tep.dao import mysql_engine


@pytest.fixture(scope="session")
def env_vars(config):
    class Clazz:
        def __init__(self):
            env = config["env"]
            self.mapping = {
                "qa": {
                    "domain": "https://qa.com",
                    "mysql_engine": mysql_engine("127.0.0.1",
                                                 "2306",
                                                 "root",
                                                 "123456",
                                                 "test")
                },
                "release": {
                    "domain": "https://release.com",
                    "mysql_engine": mysql_engine("127.0.0.1",
                                                 "2306",
                                                 "root",
                                                 "123456",
                                                 "release")
                }
            }
            self.domain = self.mapping[env]["domain"]
            self.mysql_engine = self.mapping[env]["mysql_engine"]

        def add(self, env, key, value):
            self.mapping[env][key] = value

    return Clazz()


@pytest.fixture(scope="session")
def url(env_vars, config):
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
def login():
    # Code your login

    class Clazz:
        token = ""

    return Clazz
"""

    fixture_don = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Please define your own fixture.
\"\"\"
"""

    create_folder(project_name)
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "files"))
    create_folder(os.path.join(project_name, "fixtures"))

    create_file(os.path.join(project_name, ".gitignore"), git_ignore)
    create_file(os.path.join(project_name, "conf.yaml"), conf_yaml)
    create_file(os.path.join(project_name, "conftest.py"), conftest)
    create_file(os.path.join(project_name, "pytest.ini"), pytest_ini)

    create_file(os.path.join(project_name, "tests", "__init__.py"), "")
    create_file(os.path.join(project_name, "fixtures", "__init__.py"), "")
    create_file(os.path.join(project_name, "fixtures", "fixture_admin.py"), fixture_admin)
    create_file(os.path.join(project_name, "fixtures", "fixture_don.py"), fixture_don)


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

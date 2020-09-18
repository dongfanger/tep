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

    conftest_global_content = """\"\"\" Can only be modified by the administrator. Only fixtures are provided.
\"\"\"

import os

import pytest
import yaml
from faker import Faker

_project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
def fake_ch():
    return Faker(locale='zh_CN')


@pytest.fixture(scope="session")
def fake_en():
    return Faker()


@pytest.fixture(scope="session")
def env_vars():
    class Clazz:
        def __init__(self):
            self.test_url = None

        def choose(self, env):
            if env == "qa":
                self.test_url = "https://dev.com"

            if env == "release":
                self.test_url = "https://yunke-release.qa.class100.com"

            return self

    return Clazz()


def _jwt_headers(token):
    return {"authorization": f"Bearer {token}"}


def _json_jwt_headers(token):
    return {"Content-Type": "application/json", "authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def login(env_vars, config):
    token = ""

    class Clazz:
        admin_token = token
        admin_jwt_headers = _jwt_headers(token)
        admin_json_jwt_headers = _json_jwt_headers(token)

    return Clazz
"""
    conftest_content = """\"\"\" You can customize it, if you need to share with team members, define it as a fixture.
\"\"\""""
    config_content = """env: qa"""

    ignore_content = "\n".join(
        [".idea/", ".pytest_cache/", ".tep_allure_tmp/", "__pycache__/", "*.pyc", "reports/", "debug/"]
    )

    create_folder(project_name)
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "tests", "dongfanger"))

    create_file(os.path.join(project_name, "tests", "__init__.py"), "")
    create_file(os.path.join(project_name, "tests", "conftest.py"), conftest_global_content)
    create_file(os.path.join(project_name, "tests", "dongfanger", "__init__.py"), "")
    create_file(os.path.join(project_name, "tests", "dongfanger", "conftest.py"), conftest_content)
    create_file(os.path.join(project_name, ".gitignore"), ignore_content)
    create_file(os.path.join(project_name, "conf.yaml"), config_content)


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

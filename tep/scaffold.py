#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  7/23/2020 8:12 PM
@Desc    :
"""

import os
import shutil
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

    create_folder(project_name)
    create_folder(os.path.join(project_name, "fixtures"))
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "files"))

    content = """.idea/
.pytest_cache/
.tep_allure_tmp/
__pycache__/
*.pyc
reports/
debug/"""
    create_file(os.path.join(project_name, ".gitignore"), content)

    content = """env: qa"""
    create_file(os.path.join(project_name, "conf.yaml"), content)

    content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Can only be modified by the administrator. Only fixtures are provided.
\"\"\"

import os

import pytest

# Initial
_project_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session", autouse=True)
def _project_cache(request):
    request.config.cache.set("project_dir", _project_dir)


# Auto import fixtures
_fixtures_dir = os.path.join(_project_dir, "fixtures")
for root, _, files in os.walk(_fixtures_dir):
    for file in files:
        if os.path.isfile(os.path.join(root, file)):
            if file.startswith("fixture_") and file.endswith(".py"):
                _fixture_name, _ = os.path.splitext(file)
                try:
                    exec(f"from fixtures.{_fixture_name} import *")
                except:
                    pass
"""
    create_file(os.path.join(project_name, "conftest.py"), content)

    content = """[pytest]
markers =
    smoke: smoke test
    regress: regress test
"""
    create_file(os.path.join(project_name, "pytest.ini"), content)

    content = """# Customize third-parties
# pip install --default-timeout=6000 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# mysql
pandas==1.1.0
SQLAlchemy==1.3.19
PyMySQL==0.10.0
texttable==1.6.2
"""
    create_file(os.path.join(project_name, "requirements.txt"), content)

    create_file(os.path.join(project_name, "fixtures", "__init__.py"))

    content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Can only be modified by the administrator. Only fixtures are provided.
\"\"\"

from tep.fixture import *


@pytest.fixture
def common_created_by_admin():
    pass
"""
    create_file(os.path.join(project_name, "fixtures", "fixture_admin.py"), content)

    content = """#!/usr/bin/python
# encoding=utf-8

from tep.dao import mysql_engine
from tep.fixture import *


@pytest.fixture(scope="session")
def env_vars(config):
    class Clazz(TepVars):
        env = config["env"]

        \"\"\"Variables define start\"\"\"
        # Environment and variables
        mapping = {
            "qa": {
                "domain": "https://qa.com",
                "mysql_engine": mysql_engine("127.0.0.1",  # host
                                             "2306",  # port
                                             "root",  # username
                                             "123456",  # password
                                             "qa"),  # db_name
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
        # Define properties for auto display
        domain = mapping[env]["domain"]
        mysql_engine = mapping[env]["mysql_engine"]
        \"\"\"Variables define end\"\"\"

    return Clazz()
"""
    create_file(os.path.join(project_name, "fixtures", "fixture_env_vars.py"), content)

    content = """from tep.client import request
from tep.fixture import *


def _jwt_headers(token):
    return {"Content-Type": "application/json", "authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def login(env_vars):
    # Code your login
    logger.info("Administrator login")
    response = request(
        "post",
        url=env_vars.domain + "/api/users/login",
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
"""
    create_file(os.path.join(project_name, "fixtures", "fixture_login.py"), content)

    content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Please define your own fixture.
\"\"\"

from tep.fixture import *


@pytest.fixture(scope="session")
def env_vars_your_name(config):
    class Clazz:
        env = config["env"]

        # Environment and variables
        mapping = {
            "qa": {
                "your_var": "123",
            },
            "release": {
                "your_var": "456",
            }
            # Add your environment and variables
        }
        # Define properties for auto display
        your_var = mapping[env]["your_var"]

    return Clazz()


@pytest.fixture
def share_your_name():
    pass
"""
    create_file(os.path.join(project_name, "fixtures", "fixture_your_name.py"), content)

    create_file(os.path.join(project_name, "tests", "__init__.py"))


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

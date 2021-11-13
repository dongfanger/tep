#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2021/11/13 17:50
@Desc    :  
"""

gitignore_content = """.idea/
.pytest_cache/
.tep_allure_tmp/
__pycache__/
*.pyc
reports/
debug/"""

conf_yaml_content = """env: qa"""

conftest_content = """#!/usr/bin/python
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
                try:
                    exec(f"from .fixtures.{_fixture_name} import *")
                except:
                    pass
"""

pytest_ini_content = """[pytest]
markers =
    smoke: smoke test
    regress: regress test
"""

requirements_content = """# Customize third-parties
# pip install --default-timeout=6000 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# mysql
pandas==1.1.0
SQLAlchemy==1.3.19
PyMySQL==0.10.0
texttable==1.6.2
"""

fixture_admin_content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Can only be modified by the administrator. Only fixtures are provided.
\"\"\"

from tep.fixture import *


@pytest.fixture
def common_created_by_admin():
    pass
"""

fixture_env_vars_content = """#!/usr/bin/python
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
            \"qa\": {
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

fixture_login_content = """from tep.client import request
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

fixture_your_name_content = """#!/usr/bin/python
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

test_login_content = """from loguru import logger


def test_login(login):
    logger.info(login.token)
"""

test_post_content = """import jmespath
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
"""

test_mysql_content = """from loguru import logger
from tep.dao import print_db_table


def test_mysql(pd, env_vars):
    data = pd.read_sql("select 1 from dual", env_vars.mysql_engine)
    logger.info(print_db_table(data))
"""

test_request_content = """from tep.client import request

request("get", url="", headers={}, json={})
request("post", url="", headers={}, params={})
request("put", url="", headers={}, json={})
request("delete", url="", headers={})

# upload excel
file_name = ""
file_path = ""
request("post",
        url="",
        headers={},
        files={
            "file": (
                file_name,
                open(file_path, "rb"),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        },
        verify=False
        )
"""

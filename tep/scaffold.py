#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  7/23/2020 8:12 PM
@Desc    :
"""

import os
import platform
import sys

from loguru import logger

from tep.sample import *


class ExtraArgument:
    create_venv = False


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser(
        "startproject", help="Create a new project with template structure."
    )
    sub_parser_scaffold.add_argument(
        "project_name", type=str, nargs="?", help="Specify new project name."
    )
    sub_parser_scaffold.add_argument(
        "-venv",
        dest="create_venv",
        action="store_true",
        help="Create virtual environment in the project, and install tep.",
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
                parent_path = ""
                _fixture_name, _ = os.path.splitext(file)
                fixture_path = _fixture_name
                if root != _fixtures_dir:
                    parent_path = os.path.split(root)[-1]
                    fixture_path = ".".join([parent_path, _fixture_name])
                try:
                    exec(f"from fixtures.{fixture_path} import *")
                except:
                    pass
                try:
                    exec(f"from .fixtures.{fixture_path} import *")
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

    create_folder(os.path.join(project_name, "reports"))
    create_folder(os.path.join(project_name, "utils"))
    create_folder(os.path.join(project_name, "services"))

    create_file(os.path.join(project_name, ".gitignore"), gitignore_content)
    create_file(os.path.join(project_name, "conf.yaml"), conf_yaml_content)
    create_file(os.path.join(project_name, "conftest.py"), conftest_content)
    create_file(os.path.join(project_name, "pytest.ini"), pytest_ini_content)
    create_file(os.path.join(project_name, "fixtures", "__init__.py"))
    create_file(os.path.join(project_name, "fixtures", "fixture_admin.py"), fixture_admin_content)
    create_file(os.path.join(project_name, "fixtures", "fixture_env_vars.py"), fixture_env_vars_content)
    create_file(os.path.join(project_name, "fixtures", "fixture_login.py"), fixture_login_content)
    create_file(os.path.join(project_name, "fixtures", "fixture_your_name.py"), fixture_your_name_content)
    create_file(os.path.join(project_name, "tests", "__init__.py"))
    create_file(os.path.join(project_name, "tests", "test_login.py"), test_login_content)
    create_file(os.path.join(project_name, "tests", "test_post.py"), test_post_content)
    create_file(os.path.join(project_name, "tests", "test_mysql.py"), test_mysql_content)
    create_file(os.path.join(project_name, "tests", "test_request.py"), test_request_content)
    create_file(os.path.join(project_name, "tests", "test_login_pay.py"), test_login_pay_content)
    create_file(os.path.join(project_name, "tests", "test_login_pay_httprunner.py"), test_login_pay_httprunner_content)
    create_file(os.path.join(project_name, "tests", "test_login_pay_mvc.py"), test_login_pay_mvc_content)
    create_file(os.path.join(project_name, "utils", "__init__.py"))
    create_file(os.path.join(project_name, "utils", "flask_mock_api.py"), flask_mock_api_content)
    create_file(os.path.join(project_name, "services", "__init__.py"))
    create_file(os.path.join(project_name, "services", "Login.py"), Login_content)
    create_file(os.path.join(project_name, "services", "SearchSku.py"), SearchSku_content)
    create_file(os.path.join(project_name, "services", "AddCart.py"), AddCart_content)
    create_file(os.path.join(project_name, "services", "Order.py"), Order_content)
    create_file(os.path.join(project_name, "services", "Pay.py"), Pay_content)

    if ExtraArgument.create_venv:
        os.chdir(project_name)
        print("\nCreating virtual environment")
        os.system("python -m venv .venv")
        print("Created virtual environment: .venv")

        print("Installing tep")
        if platform.system().lower() == 'windows':
            os.chdir(".venv")
            os.chdir("Scripts")
            os.system("pip install tep")
        elif platform.system().lower() == 'linux':
            os.chdir(".venv")
            os.chdir("bin")
            os.system("pip install tep")


def main_scaffold(args):
    ExtraArgument.create_venv = args.create_venv
    sys.exit(create_scaffold(args.project_name))

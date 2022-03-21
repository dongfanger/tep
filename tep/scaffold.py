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
    """命令行附加参数映射
    """
    # 是否创建Python虚拟环境
    create_venv = False


def init_parser_scaffold(subparsers):
    """定义参数
    """
    sub_parser_scaffold = subparsers.add_parser("startproject", help="Create a new project with template structure.")
    sub_parser_scaffold.add_argument("project_name", type=str, nargs="?", help="Specify new project name.")
    sub_parser_scaffold.add_argument(
        "-venv",
        dest="create_venv",
        action="store_true",
        help="Create virtual environment in the project, and install tep.",
    )
    return sub_parser_scaffold


def create_scaffold(project_name):
    """ 创建项目脚手架
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
        msg = f"Created file:   {path}"
        print(msg)

    create_folder(project_name)
    create_folder(os.path.join(project_name, "files"))
    create_folder(os.path.join(project_name, "fixtures"))
    create_file(os.path.join(project_name, "fixtures", "__init__.py"))
    create_file(os.path.join(project_name, "fixtures", "fixture_env_vars.py"), fixture_env_vars_content)
    create_file(os.path.join(project_name, "fixtures", "fixture_login.py"), fixture_login_content)
    create_folder(os.path.join(project_name, "reports"))
    create_folder(os.path.join(project_name, "samples"))
    create_file(os.path.join(project_name, "samples", "__init__.py"))
    create_folder(os.path.join(project_name, "samples", "assert"))
    create_file(os.path.join(project_name, "samples", "assert", "__init__.py"))
    create_file(os.path.join(project_name, "samples", "assert", "test_assert.py"), test_assert)
    create_folder(os.path.join(project_name, "samples", "db"))
    create_file(os.path.join(project_name, "samples", "db", "__init__.py"))
    create_file(os.path.join(project_name, "samples", "db", "test_mysql.py"), test_mysql_content)
    create_folder(os.path.join(project_name, "samples", "http"))
    create_file(os.path.join(project_name, "samples", "http", "__init__.py"))
    create_file(os.path.join(project_name, "samples", "http", "test_request.py"), test_request_content)
    create_file(os.path.join(project_name, "samples", "http", "test_request_monkey_patch.py"),
                test_request_monkey_patch_content)
    create_folder(os.path.join(project_name, "samples", "login_pay"))
    create_file(os.path.join(project_name, "samples", "login_pay", "__init__.py"))
    create_folder(os.path.join(project_name, "samples", "login_pay", "mvc"))
    create_file(os.path.join(project_name, "samples", "login_pay", "mvc", "__init__.py"))
    create_file(os.path.join(project_name, "samples", "login_pay", "mvc", "test_login_pay_mvc.py"),
                test_login_pay_mvc_content)
    create_folder(os.path.join(project_name, "samples", "login_pay", "mvc", "services"))
    create_file(os.path.join(project_name, "samples", "login_pay", "mvc", "services", "__init__.py"))
    create_file(os.path.join(project_name, "samples", "login_pay", "mvc", "services", "AddCart.py"), AddCart_content)
    create_file(os.path.join(project_name, "samples", "login_pay", "mvc", "services", "Login.py"), Login_content)
    create_file(os.path.join(project_name, "samples", "login_pay", "mvc", "services", "Order.py"), Order_content)
    create_file(os.path.join(project_name, "samples", "login_pay", "mvc", "services", "Pay.py"), Pay_content)
    create_file(os.path.join(project_name, "samples", "login_pay", "mvc", "services", "SearchSku.py"),
                SearchSku_content)
    create_folder(os.path.join(project_name, "samples", "login_pay", "tep"))
    create_file(os.path.join(project_name, "samples", "login_pay", "tep", "__init__.py"))
    create_file(os.path.join(project_name, "samples", "login_pay", "tep", "test_login.py"), test_login_content)
    create_file(os.path.join(project_name, "samples", "login_pay", "tep", "test_login_pay.py"), test_login_pay_content)
    create_folder(os.path.join(project_name, "tests"))
    create_file(os.path.join(project_name, "tests", "__init__.py"))
    create_folder(os.path.join(project_name, "utils"))
    create_file(os.path.join(project_name, "utils", "__init__.py"))
    create_file(os.path.join(project_name, "utils", "fastapi_mock.py"), fastapi_mock_content)
    create_file(os.path.join(project_name, "utils", "http_client.py"), http_client_content)
    create_file(os.path.join(project_name, "utils", "mitm.py"), mitm_content)
    create_file(os.path.join(project_name, ".gitignore"), gitignore_content)
    create_file(os.path.join(project_name, "conf.yaml"), conf_yaml_content)
    create_file(os.path.join(project_name, "conftest.py"), conftest_content)
    create_file(os.path.join(project_name, "pytest.ini"), pytest_ini_content)
    create_file(os.path.join(project_name, "项目结构说明.txt"), structure_content)

    if ExtraArgument.create_venv:
        # 创建Python虚拟环境
        os.chdir(project_name)
        print("\nCreating virtual environment")
        os.system("python -m venv .venv")
        print("Created virtual environment: .venv")

        # 在Python虚拟环境中安装tep
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

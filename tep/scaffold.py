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

    def read_demo(path):
        with open(path) as f:
            return f.read()

    demo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo")

    git_ignore = read_demo(os.path.join(demo_path, ".gitignore"))
    conf_yaml = read_demo(os.path.join(demo_path, "conf.yaml"))
    conftest = read_demo(os.path.join(demo_path, "conftest.py"))
    pytest_ini = read_demo(os.path.join(demo_path, "pytest.ini"))
    fixture_admin = read_demo(os.path.join(demo_path, "fixtures", "fixture_admin.py"))
    fixture_your_name = read_demo(os.path.join(demo_path, "fixtures", "fixture_your_name.py"))
    login_test = read_demo(os.path.join(demo_path, "tests", "login_test.py"))

    create_folder(project_name)
    create_folder(os.path.join(project_name, "fixtures"))
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "files"))

    create_file(os.path.join(project_name, ".gitignore"), git_ignore)
    create_file(os.path.join(project_name, "conf.yaml"), conf_yaml)
    create_file(os.path.join(project_name, "conftest.py"), conftest)
    create_file(os.path.join(project_name, "pytest.ini"), pytest_ini)

    create_file(os.path.join(project_name, "fixtures", "__init__.py"), "")
    create_file(os.path.join(project_name, "fixtures", "fixture_admin.py"), fixture_admin)
    create_file(os.path.join(project_name, "fixtures", "fixture_your_name.py"), fixture_your_name)

    create_file(os.path.join(project_name, "tests", "__init__.py"), "")
    create_file(os.path.join(project_name, "tests", "login_test.py"), login_test)


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

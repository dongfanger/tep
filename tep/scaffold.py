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

    conftest_content = """import os

import pytest


project_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session", autouse=True)
def project_cache(request):
    request.config.cache.set("project_dir", project_dir)


class Dev:
    test_url = 'https://dev.com'


class Qa:
    test_url = 'https://qa.com'


class Release:
    test_url = 'https://release.com'


# choose environment
env = Qa

# you can define your variables and functions and so on
"""

    ignore_content = "\n".join(
        [".idea/", ".pytest_cache/", "__pycache__/", "*.pyc", "reports/", "debug/"]
    )

    create_folder(project_name)
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "tests", "dongfanger"))

    create_file(os.path.join(project_name, "tests", "__init__.py"), "")
    create_file(os.path.join(project_name, "tests", "dongfanger", "__init__.py"), "")
    create_file(os.path.join(project_name, "conftest.py"), conftest_content)
    create_file(os.path.join(project_name, ".gitignore"), ignore_content)


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

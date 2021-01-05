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

from tep import __version__


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

    def copy_demo_file(relative_path, filename):
        tep_demo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo")
        src = os.path.join(tep_demo_path, relative_path, filename)
        des = os.path.join(project_name, relative_path)
        shutil.copy(src, des)
        msg = f"Created file: {os.path.join(des, filename)}"
        print(msg)

    create_folder(project_name)
    create_folder(os.path.join(project_name, "fixtures"))
    create_folder(os.path.join(project_name, "tests"))
    create_folder(os.path.join(project_name, "tests", "sample"))
    create_folder(os.path.join(project_name, "tests", "sample", "case_reuse"))
    create_folder(os.path.join(project_name, "files"))

    copy_demo_file("", ".gitignore")
    copy_demo_file("", "conf.yaml")
    copy_demo_file("", "conftest.py")
    copy_demo_file("", "pytest.ini")

    create_file(os.path.join(project_name, "fixtures", "__init__.py"))
    copy_demo_file("fixtures", "fixture_admin.py")
    copy_demo_file("fixtures", "fixture_login.py")
    copy_demo_file("fixtures", "fixture_your_name.py")

    create_file("tests", "__init__.py")
    copy_demo_file(os.path.join("tests", "sample"), "login_test.py")
    copy_demo_file(os.path.join("tests", "sample"), "mysql_test.py")
    copy_demo_file(os.path.join("tests", "sample"), "post_test.py")
    copy_demo_file(os.path.join("tests", "sample"), "var_reuse_test.py")

    create_file(os.path.join(project_name, "tests", "sample", "case_reuse", "__init__.py"))
    copy_demo_file(os.path.join("tests", "sample", "case_reuse"), "a_test.py")
    copy_demo_file(os.path.join("tests", "sample", "case_reuse"), "reuse_a_test.py")


def update_scaffold():
    def create_folder(path):
        os.makedirs(path)
        msg = f"Created folder: {path}"
        print(msg)

    def copy_demo_file(relative_path, filename, des):
        tep_demo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo")
        src = os.path.join(tep_demo_path, relative_path, filename)
        shutil.copy(src, des)
        msg = f"Updated file: {os.path.join(des, filename)}"
        print(msg)

    if not os.path.exists("conftest.py"):
        logger.warning("tep project not found, please relocate to the tep project which contains a conftest.py file.")
        return

    if __version__ >= "0.6.0":
        version_dir = f"version{__version__}"
        version_fixtures_dir = os.path.join(version_dir, "fixtures-upgrade")
        if os.path.exists(version_dir):
            logger.warning("Version directory exists, please delete first.")
            return
        create_folder(version_dir)

        create_folder(version_fixtures_dir)
        copy_demo_file("fixtures", "fixture_admin.py", des=version_fixtures_dir)
        copy_demo_file("fixtures", "fixture_login.py", des=version_fixtures_dir)
        copy_demo_file("fixtures", "fixture_your_name.py", des=version_fixtures_dir)

        copy_demo_file("", "conftest.py", des=os.getcwd())
    else:
        logger.info("There is no need to upgrade scaffold, please check the version of tep.")
        return


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

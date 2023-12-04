#!/usr/bin/python
# encoding=utf-8

import os
import platform
import sys

from loguru import logger

from tep.libraries.Config import Config


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser("new", help="Create a new project with template structure.")
    sub_parser_scaffold.add_argument("project_name", type=str, nargs="?", help="Specify new project name.")
    sub_parser_scaffold.add_argument(
        "-venv",
        dest="create_venv",
        action="store_true",
        help="Create virtual environment in the project, and install tep.",
    )
    return sub_parser_scaffold


def scaffold(args):
    Config.CREATE_ENV = args.create_venv
    sys.exit(create_scaffold(args.project_name))


def create_scaffold(project_name):
    if os.path.isdir(project_name):
        logger.warning(f"Project folder {project_name} exists, please specify a new project name")
        return 1
    elif os.path.isfile(project_name):
        logger.warning(f"Project name {project_name} conflicts with existed file, please specify a new one")
        return 1

    print(f"Create new project: {project_name}")
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
    create_folder(os.path.join(project_name, "case"))
    create_folder(os.path.join(project_name, "data"))
    create_folder(os.path.join(project_name, "data", "har"))
    create_folder(os.path.join(project_name, "report"))

    replay_content = """import os

from tep.libraries.Config import Config
from tep.libraries.Har import Har

if __name__ == '__main__':
    profile = {
        "harDir": os.path.join(Config.BASE_DIR, "data", "har"),
        "desDir": os.path.join(Config.BASE_DIR, "case", "replay")
    }
    Har(profile).har2case()
"""
    create_file(os.path.join(project_name, "replay.py"), replay_content)
    run_content = """from tep.libraries.Run import Run

if __name__ == '__main__':
    settings = {
        "path": ["test_demo.py"],  # Path to run, relative path to case
        "report": False,  # Output test report or not
        "report_type": "pytest-html"  # "pytest-html" "allure"
    }
    Run(settings)
"""
    create_file(os.path.join(project_name, "run.py"), run_content)
    conftest_content = """from tep.plugin import tep_plugins

pytest_plugins = tep_plugins()
"""
    create_file(os.path.join(project_name, "conftest.py"), conftest_content)
    create_file(os.path.join(project_name, "pytest.ini"), "")
    gitignore_content = """.idea
.pytest_cache/
__pycache__/
.har
"""
    create_file(os.path.join(project_name, ".gitignore"), gitignore_content)
    create_file(os.path.join(project_name, "case", "__init__.py"), "")
    demo_content = """def test(HTTPRequestKeyword):
    response = HTTPRequestKeyword("get", url="http://httpbin.org/status/200")
    assert response.status_code == 200
"""
    create_file(os.path.join(project_name, "case", "test_demo.py"), demo_content)
    user_defined_variables_content = 'name: "公众号测试开发刚哥"'
    create_file(os.path.join(project_name, "data", "UserDefinedVariables.yaml"), user_defined_variables_content)

    if Config.CREATE_ENV:
        # Create Python virtual Environment
        os.chdir(project_name)
        print("\nCreating virtual environment")
        os.system("python -m venv .venv")
        print("Created virtual environment: .venv")

        # Install tep in the Python virtual Environment
        print("Installing tep")
        if platform.system().lower() == 'windows':
            os.chdir(".venv")
            os.chdir("Scripts")
            os.system("pip install tep")
        elif platform.system().lower() == 'linux':
            os.chdir(".venv")
            os.chdir("bin")
            os.system("pip install tep")

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
        'startproject', help='create a new project with template structure.'
    )
    sub_parser_scaffold.add_argument(
        'project_name', type=str, nargs='?', help='specify new project name.'
    )
    return sub_parser_scaffold


def create_scaffold(project_name):
    """ create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        logger.warning(
            f'project folder {project_name} exists, please specify a new project name.'
        )
        return 1
    elif os.path.isfile(project_name):
        logger.warning(
            f'project name {project_name} conflicts with existed file, please specify a new one.'
        )
        return 1

    logger.info(f'create new project: {project_name}')
    print(f'project root dir: {os.path.join(os.getcwd(), project_name)}\n')

    def create_folder(path):
        os.makedirs(path)
        msg = f'created folder: {path}'
        print(msg)

    def create_file(path, file_content=''):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        msg = f'created file: {path}'
        print(msg)

    run_content = """import os
import shutil

from tep.funcs import current_date

project_dir = os.path.dirname(os.path.abspath(__file__))

api_dir = os.path.join(project_dir, 'api')

testcases_dir = os.path.join(project_dir, 'testcases')

datafiles_dir = os.path.join(project_dir, 'datafiles')

reports_dir = os.path.join(project_dir, 'reports')

log_file = os.path.join(reports_dir, current_date() + '.log')

api_record_file = os.path.join(reports_dir, "api-record-" + current_date() + ".csv")

allure_report_dir = os.path.join(reports_dir, 'report-' + current_date())

# choose path to run tests
run_dir = os.path.join(testcases_dir, '')

# open allure test report automatically after testing
open_allure_report = 1

if __name__ == '__main__':

    if os.path.exists(allure_report_dir):
        shutil.rmtree(allure_report_dir)
    os.makedirs(allure_report_dir)

    os.system(f'pytest -v {run_dir} --alluredir {allure_report_dir}')
"""

    conftest_content = """import os

from run import open_allure_report


def pytest_sessionfinish(session):
    allure_report_dir = session.config.getoption('allure_report_dir')
    if allure_report_dir:
        html_dir = os.path.join(allure_report_dir, 'html')
        os.system(f'mkdir {html_dir}')
        os.system(f"allure generate {allure_report_dir} -o {html_dir}")
        if open_allure_report:
            os.system(f"allure open {html_dir}")"""

    testcases_conftest_content = """

def token_headers(token):
    return {"Content-Type": "application/json", "token": token}


headers = {"Content-Type": "application/json"}


class Dev:
    test_url = 'https://dev.com'
    # dao_x = Dao('host:port',
    #             'username',
    #             'password')


class Qa:
    test_url = 'https://qa.com'
    # dao_x = Dao('host:port',
    #             "username",
    #             "password")


class Release:
    test_url = 'https://release.com'
    # dao_x = Dao('host:port',
    #             "username",
    #             "password")


# choose environment
env = Release
"""

    ignore_content = '\n'.join(
        ['.idea/', '.pytest_cache/', '__pycache__/', '*.pyc', 'reports/report*/', 'reports/*.log', 'debug/']
    )

    create_folder(project_name)
    create_folder(os.path.join(project_name, 'testcases'))
    create_folder(os.path.join(project_name, 'datafiles'))
    create_folder(os.path.join(project_name, 'reports'))

    create_file(os.path.join(project_name, 'testcases', '__init__.py'), '')
    create_file(os.path.join(project_name, 'testcases', 'conftest.py'), testcases_conftest_content)
    create_file(os.path.join(project_name, 'run.py'), run_content)
    create_file(os.path.join(project_name, 'conftest.py'), conftest_content)
    create_file(os.path.join(project_name, '.gitignore'), ignore_content)


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

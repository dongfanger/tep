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
        'startproject', help='Create a new project with template structure.'
    )
    sub_parser_scaffold.add_argument(
        'project_name', type=str, nargs='?', help='Specify new project name.'
    )
    return sub_parser_scaffold


def create_scaffold(project_name):
    """ Create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        logger.warning(
            f'Project folder {project_name} exists, please specify a new project name.'
        )
        return 1
    elif os.path.isfile(project_name):
        logger.warning(
            f'Project name {project_name} conflicts with existed file, please specify a new one.'
        )
        return 1

    logger.info(f'Create new project: {project_name}')
    print(f'Project root dir: {os.path.join(os.getcwd(), project_name)}\n')

    def create_folder(path):
        os.makedirs(path)
        msg = f'Created folder: {path}'
        print(msg)

    def create_file(path, file_content=''):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        msg = f'Created file: {path}'
        print(msg)

    conftest_content = """import os
import shutil

import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_pytest.listener import AllureListener
from allure_pytest.plugin import cleanup_factory
from tep.funcs import current_date

project_dir = os.path.dirname(os.path.abspath(__file__))

_reports_html = os.path.join(project_dir, 'reports', 'report-' + current_date())

_allure_temp = '.allure-temp-auto-del'


def pytest_addoption(parser):
    parser.addoption(
        '--tep-reports',
        action='store_const',
        const=True,
        help='Create tep reports and open automatically.'
    )


def _tep_reports(config):
    if config.getoption('--tep-reports') and not config.getoption('allure_report_dir'):
        return True
    else:
        return False


def pytest_configure(config):
    if _tep_reports(config):
        test_listener = AllureListener(config)
        config.pluginmanager.register(test_listener)
        allure_commons.plugin_manager.register(test_listener)
        config.add_cleanup(cleanup_factory(test_listener))

        clean = config.option.clean_alluredir
        file_logger = AllureFileLogger(_allure_temp, clean)
        allure_commons.plugin_manager.register(file_logger)
        config.add_cleanup(cleanup_factory(file_logger))


def pytest_sessionfinish(session):
    if _tep_reports(session.config):
        os.system(f"allure generate {_allure_temp} -o {_reports_html}  --clean")
        shutil.rmtree(_allure_temp)
        os.system(f"allure open {_reports_html}")
"""

    testcases_conftest_content = """from faker import Faker
from loguru import logger


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


def json_token_headers(token):
    return {"Content-Type": "application/json", "token": token}


def token_headers(token):
    return {"token": token}


headers = {"Content-Type": "application/json"}
fake = Faker(locale='zh_CN')

logger.info('admin login to get token')
admin_login_token = 'token'
admin_json_token_headers = json_token_headers(admin_login_token)
admin_token_headers = token_headers(admin_login_token)
"""

    crud_test_content = """import jmespath
from loguru import logger
from testcases.conftest import fake, env

from prj.testcases.conftest import admin_json_token_headers
from tep.client import request


def test():
    logger.info('create')
    test_name = fake.name()
    response = request(
        'post',
        url=env.test_url + '/api',
        headers=admin_json_token_headers,
        json={
            "name": test_name
        }
    )
    assert response.status_code < 400

    logger.info('retrieve')
    response = request(
        'get',
        url=env.test_url + '/api',
        headers=admin_json_token_headers,
        params={
            "keyword": test_name
        }
    )
    assert response.status_code < 400
    test_id = jmespath.search('id', response.json())

    logger.info('update')
    response = request(
        'put',
        url=env.test_url + f'/api/{test_id}',
        headers=admin_json_token_headers,
        json={
            "name": test_name + '-update'
        }
    )
    assert response.status_code < 400

    logger.info('delete')
    response = request(
        'delete',
        url=env.test_url + f'/api/{test_id}',
        headers=admin_json_token_headers
    )
    assert response.status_code < 400
"""

    ignore_content = '\n'.join(
        ['.idea/', '.pytest_cache/', '__pycache__/', '*.pyc', 'reports/report*/', 'reports/*.log', 'debug/']
    )

    create_folder(project_name)
    create_folder(os.path.join(project_name, 'testcases'))

    create_file(os.path.join(project_name, 'testcases', '__init__.py'), '')
    create_file(os.path.join(project_name, 'testcases', 'conftest.py'), testcases_conftest_content)
    create_file(os.path.join(project_name, 'testcases', 'crud_test.py'), crud_test_content)
    create_file(os.path.join(project_name, 'conftest.py'), conftest_content)
    create_file(os.path.join(project_name, '.gitignore'), ignore_content)


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

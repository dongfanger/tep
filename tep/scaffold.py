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


tep_dir = os.path.dirname(os.path.abspath(__file__))


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

    ignore_content = '\n'.join(
        ['.idea/', '.pytest_cache/', '__pycache__/', '*.pyc', 'reports/report*/', 'reports/*.log', 'debug/']
    )

    create_folder(project_name)
    create_folder(os.path.join(project_name, 'tests'))

    create_file(os.path.join(project_name, 'tests', '__init__.py'), '')
    create_file(os.path.join(project_name, 'conftest.py'), conftest_content)
    create_file(os.path.join(project_name, '.gitignore'), ignore_content)


def main_scaffold(args):
    sys.exit(create_scaffold(args.project_name))

#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  8/14/2020 9:16 AM
@Desc    :  
"""
import os
import pickle
import shutil

import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_pytest.listener import AllureListener
from allure_pytest.plugin import cleanup_factory

from tep.funcs import current_date
from tep.scaffold import tep_dir

with open(os.path.join(tep_dir, 'files', 'project_dir'), 'rb') as f:
    project_dir = pickle.load(f)

_reports_html = os.path.join(project_dir, 'reports', 'report-' + current_date())

_allure_temp = '.allure-temp-auto-del'


def _tep_reports(config):
    if config.getoption('--tep-reports') and not config.getoption('allure_report_dir'):
        return True
    else:
        return False


class Plugin:

    def pytest_addoption(parser):
        parser.addoption(
            '--tep-reports',
            action='store_const',
            const=True,
            help='Create tep reports and open automatically.'
        )

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

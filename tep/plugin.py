#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  8/14/2020 9:16 AM
@Desc    :  
"""

import os
import shutil

import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_pytest.listener import AllureListener
from allure_pytest.plugin import cleanup_factory

from tep.funcs import current_time

allure_temp = "tep_allure.tmp"


class Plugin:
    @staticmethod
    def pytest_addoption(parser):
        parser.addoption(
            '--tep-reports',
            action='store_const',
            const=True,
            help='Create tep reports and open automatically.'
        )

    @staticmethod
    def _tep_reports(config):
        if config.getoption('--tep-reports') and not config.getoption('allure_report_dir'):
            return True
        else:
            return False

    @staticmethod
    def pytest_configure(config):
        if Plugin._tep_reports(config):
            test_listener = AllureListener(config)
            config.pluginmanager.register(test_listener)
            allure_commons.plugin_manager.register(test_listener)
            config.add_cleanup(cleanup_factory(test_listener))

            clean = config.option.clean_alluredir
            file_logger = AllureFileLogger(allure_temp, clean)
            allure_commons.plugin_manager.register(file_logger)
            config.add_cleanup(cleanup_factory(file_logger))

    @staticmethod
    def pytest_sessionfinish(session):
        if Plugin._tep_reports(session.config):
            project_dir = session.config.cache.get("project_dir", None)
            reports_dir = os.path.join(project_dir, 'reports')
            new_report = os.path.join(reports_dir, 'report-' + current_time().replace(":", "-").replace(" ", "-"))
            his_reports = os.listdir(reports_dir)
            if his_reports:
                latest_report_history = os.path.join(reports_dir, his_reports[-1], "history")
                shutil.copytree(latest_report_history, os.path.join(allure_temp, "history"))
            os.system(f"allure generate {allure_temp} -o {new_report}  --clean")
            shutil.rmtree(allure_temp)

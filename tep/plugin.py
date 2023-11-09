#!/usr/bin/python
# encoding=utf-8
import inspect
import os
import shutil

import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_pytest.listener import AllureListener
from allure_pytest.plugin import cleanup_factory

from tep.libraries.Config import Config


def tep_plugins():
    """
    Must be placed at the top, execute first to initialize base dir
    """
    caller = inspect.stack()[1]
    Config.BASE_DIR = os.path.abspath(os.path.dirname(caller.filename))
    plugins = _keyword_path() + _fixture_path()  # +[other plugins]
    return plugins


def _tep_reports(config):
    """
    --tep-reports cannot be used together with the allure command line parameter, otherwise an error may occur
    """
    if config.getoption("--tep-reports") and not config.getoption("allure_report_dir"):
        return True
    return False


def _is_master(config):
    """
    During pytest-xdist distributed execution, determine whether it is the master node or a child node
    The main node does not have a workerinput attribute
    config: session.config
    """
    return not hasattr(config, 'workerinput')


def _keyword_path() -> list:
    return ["tep.keywords.api"]


def _fixture_path():
    _fixture_dir = os.path.join(Config.BASE_DIR, "fixture")
    paths = []
    # 项目下的fixtures
    for root, _, files in os.walk(_fixture_dir):
        for file in files:
            if file.startswith("fixture_") and file.endswith(".py"):
                full_path = os.path.join(root, file)
                import_path = full_path.replace(_fixture_dir, "").replace("\\", ".")
                import_path = import_path.replace("/", ".").replace(".py", "")
                paths.append("fixture" + import_path)
    return paths


class Plugin:
    @staticmethod
    def pytest_addoption(parser):
        """
        Allure test report, command line parameters
        """
        parser.addoption(
            "--tep-reports",
            action="store_const",
            const=True,
            help="Create tep allure HTML reports."
        )

    @staticmethod
    def pytest_configure(config):
        """
        Reference: https://github.com/allure-framework/allure-python/blob/master/allure-pytest/src/plugin.py
        In order to generate an allure source file for generating HTML reports
        """
        if _tep_reports(config):
            if os.path.exists(Config.ALLURE_SOURCE_PATH):
                shutil.rmtree(Config.ALLURE_SOURCE_PATH)
            test_listener = AllureListener(config)
            config.pluginmanager.register(test_listener)
            allure_commons.plugin_manager.register(test_listener)
            config.add_cleanup(cleanup_factory(test_listener))

            clean = config.option.clean_alluredir
            file_logger = AllureFileLogger(Config.ALLURE_SOURCE_PATH, clean)  # allure_source
            allure_commons.plugin_manager.register(file_logger)
            config.add_cleanup(cleanup_factory(file_logger))

    @staticmethod
    def pytest_sessionfinish(session):
        """
        Generate an allure report after the test run ends
        """
        reports_path = os.path.join(Config.BASE_DIR, "reports")
        if _tep_reports(session.config):
            if _is_master(session.config):  # Generate reports only at the master node
                # Historical data from the latest report, filling in the allure trend chart
                if os.path.exists(reports_path):
                    his_reports = os.listdir(reports_path)
                    if his_reports:
                        latest_report_history = os.path.join(reports_path, his_reports[-1], "history")
                        shutil.copytree(latest_report_history, os.path.join(Config.ALLURE_SOURCE_PATH, "history"))

                os.system(f"allure generate {Config.ALLURE_SOURCE_PATH} -o {Config().HTML_REPORT_PATH}  --clean")
                shutil.rmtree(Config.ALLURE_SOURCE_PATH)

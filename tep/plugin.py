#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  dongfanger
@Date    :  8/14/2020 9:16 AM
@Desc    :  插件
"""

import os
import shutil
import tempfile

import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_pytest.listener import AllureListener
from allure_pytest.plugin import cleanup_factory

from tep import func
from tep.fixture import Project

# allure临时目录
allure_temp = tempfile.mkdtemp()


class Plugin:
    @staticmethod
    def pytest_addoption(parser):
        # allure测试报告 命令行参数
        parser.addoption(
            "--tep-reports",
            action="store_const",
            const=True,
            help="Create tep allure HTML reports."
        )

    @staticmethod
    def _tep_reports(config):
        # 判断参数是否生效，防止跟allure自带参数冲突
        if config.getoption("--tep-reports") and not config.getoption("allure_report_dir"):
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
        # 测试运行结束后生成allure报告
        if Plugin._tep_reports(session.config):
            reports_dir = os.path.join(Project.dir, "reports")
            new_report = os.path.join(reports_dir,
                                      "report-" + func.time_current().replace(":", "-").replace(" ", "-"))
            if os.path.exists(reports_dir):
                # 复制历史报告，填充allure趋势图数据
                his_reports = os.listdir(reports_dir)
                if his_reports:
                    latest_report_history = os.path.join(reports_dir, his_reports[-1], "history")
                    shutil.copytree(latest_report_history, os.path.join(allure_temp, "history"))
            os.system(f"allure generate {allure_temp} -o {new_report}  --clean")
            shutil.rmtree(allure_temp)

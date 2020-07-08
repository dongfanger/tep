#!/usr/bin/python
# encoding=utf-8

"""
@Author : dongfanger
@Date   : 2020/3/7 11:33
@Desc   : after testing, auto generate allure test report and open
"""

import os
from pytest_allure import open_allure_report


def pytest_sessionstart(session):
    pass


def pytest_sessionfinish(session):
    allure_report_dir_test = session.config.getoption('allure_report_dir')
    if allure_report_dir_test:
        html_dir = os.path.join(allure_report_dir_test, 'html')
        os.system(f'mkdir {html_dir}')
        os.system(f"allure generate {allure_report_dir_test} -o {html_dir}")
        if open_allure_report:
            os.system(f"allure open {html_dir}")

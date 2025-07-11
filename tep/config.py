#!/usr/bin/python
# encoding=utf-8

import os
import time


class Config:
    # Class variable initialize first
    BASE_DIR = ''  # Project root directory, project -> conftest.py -> plugin.py -> assign

    CREATE_VENV = False
    TEP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self):
        # Instance variable initialize after class variable assigned
        self.TESTS_DIR = os.path.join(self.BASE_DIR, 'tests')
        self.DATA_DIR = os.path.join(self.BASE_DIR, 'data')
        self.FILE_DIR = os.path.join(self.BASE_DIR, 'file')
        self.REPORT_DIR = os.path.join(self.BASE_DIR, 'report')
        self.FIXTURE_DIR = os.path.join(self.BASE_DIR, 'fixture')
        self.LOG_DIR = os.path.join(self.BASE_DIR, 'log')

        current_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
        self.HTML_REPORT_PATH = os.path.join(self.REPORT_DIR, 'report-' + current_time)

    @classmethod
    def get_project_dir(cls):
        tests = 'tests'
        current_path = os.getcwd().split(os.path.sep)
        try:
            i = current_path.index(tests)
            return os.path.sep.join(current_path[:i])  # tests parent dir
        except ValueError:
            return ''
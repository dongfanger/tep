#!/usr/bin/python
# encoding=utf-8

import os
import time


class Config:
    # Class variable initialize first
    BASE_DIR = ""

    # Constant
    CREATE_ENV = False
    # The temporary directory of the allure source file, which is a pile of JSON files,
    # will be deleted when generating HTML reports
    ALLURE_SOURCE_PATH = ".allure.source.temp"

    def __init__(self):
        # Instance variable initialize after class variable assigned
        self.CASE_DIR = os.path.join(self.BASE_DIR, "case")
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")
        self.REPORT_DIR = os.path.join(self.BASE_DIR, "report")

        current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        self.HTML_REPORT_PATH = os.path.join(self.REPORT_DIR, "report-" + current_time)


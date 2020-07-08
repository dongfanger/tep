#!/usr/bin/python
# encoding=utf-8

"""
@Author : dongfanger
@Date   : 2020/2/28 17:06
@Desc   : run pytest by batch and generate allure report
"""

import os
import shutil

from common.func import current_time
from config.relative_path import result_dir

# options
from data.env import *

# choose environment name
vars_ = Qa

# 1:develop 2:online(return 1 random for efficiency)
pare_wise_mode = 1

# 0:no log & no record 1:log 2:record 3:log & record
api_log_level = 1

# open allure report after test
open_allure_report = 0


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    result_report_dir = os.path.join(result_dir, 'report-' + current_time('date'))
    if os.path.exists(result_report_dir):
        shutil.rmtree(result_report_dir)
    os.makedirs(result_report_dir)

    # input the directory to run pytest
    run_dir = os.path.join(base_dir, 'case')

    os.system(f'pytest -v {run_dir} --alluredir {result_report_dir}')

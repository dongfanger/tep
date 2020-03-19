#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   : 2020/2/28 17:06
@Desc   : Run pytest by batch and generate allure report
"""

import os

from common.func import current_time
from config.relative_path import result_dir

base_dir = os.path.dirname(os.path.abspath(__file__))
result_report_dir = os.path.join(result_dir, 'report-' + current_time('date'))
if os.path.exists(result_report_dir):
    os.system(f'rm -rf {result_report_dir}')
os.system(f'mkdir {result_report_dir}')

# Input the directory to run pytest
run_dir = os.path.join(base_dir, 'case')
os.system(f'pytest -v {run_dir} --alluredir {result_report_dir}')

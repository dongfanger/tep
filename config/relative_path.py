#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   : 2019/12/12 10:58
@Desc   : Relative path
"""

import os
import time

current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

result_dir = os.path.join(base_dir, 'result')

case_dir = os.path.join(current_date, 'case')

data_dir = os.path.join(current_date, 'data')

log_file = os.path.join(result_dir, current_date + '.log')

html_report_file = os.path.join(result_dir, '自动化测试报告' + current_date + '.html')

interface_called_info_file = os.path.join(result_dir, "接口调用记录" + current_date + ".csv")

# Csv data storage
recent_20_days_file = os.path.join(current_date, 'recent-20-days.csv')



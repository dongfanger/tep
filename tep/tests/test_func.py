#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  dongfanger
@Date    :  5/16/2022 5:41 PM
@Desc    :  常用函数
"""

from tep import func


def test_data():
    """造数据"""
    print(func.data_fake().name())  # 姓名
    print(func.data_textbox())  # 文本输入框各类型数据


def test_time():
    """时间日期"""
    print(func.time_current())  # 2022-05-19 21:55:21
    print(func.time_current("date"))  # 2022-05-19


def test_print():
    """打印文本"""
    for i in range(101):
        print(func.print_progress_bar(i))  # 99% [■■■■■■■■■□]


def test_case():
    """测试用例"""
    pl = [['M', 'O', 'P'], ['W', 'L', 'I'], ['C', 'E']]
    a = func.case_pairwise(pl)
    print()
    for i in a:
        print(i)

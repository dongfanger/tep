#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  dongfanger
@Date    :  7/24/2020 5:41 PM
@Desc    :  tep函数库
"""
import copy
import itertools
import json
import os
import time
from sys import stdout

from faker import Faker
from loguru import logger

# ---------------- 模块变量开始 ---------------------
tep_dir = os.path.dirname(os.path.abspath(__file__))
files_dir = os.path.join(tep_dir, "files")


# ---------------- 模块变量开始 ---------------------


# ---------------- 造数据开始 ---------------------
def data_fake(locale="zh_CN"):
    """造数据，默认中文"""
    return Faker(locale)


def data_textbox():
    """文本框输入数据"""
    with open(os.path.join(files_dir, "文本框输入数据.txt")) as f:
        return f.read().splitlines()


# ---------------- 造数据结束 ---------------------


# ---------------- 时间日期开始 ---------------------
def time_current(format_="time"):
    """当前时间"""
    mapping = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
        "date": time.strftime("%Y-%m-%d", time.localtime(time.time()))
    }
    return mapping[format_]


# ---------------- 时间日期结束 ---------------------


# ---------------- 打印文本开始 ---------------------
def print_progress_bar(i):
    """进度条"""
    c = int(i / 10)
    progress = '\r %2d%% [%s%s]'
    a = '■' * c
    b = '□' * (10 - c)
    msg = progress % (i, a, b)
    stdout.write(msg)
    stdout.flush()


# ---------------- 打印文本结束 ---------------------


# ---------------- 测试用例开始 ---------------------
def case_pairwise(option):
    """pairwise算法"""
    cp = []  # 笛卡尔积
    s = []  # 两两拆分
    for x in eval('itertools.product' + str(tuple(option))):
        cp.append(x)
        s.append([i for i in itertools.combinations(x, 2)])
    logger.info('笛卡尔积:%s' % len(cp))
    del_row = []
    print_progress_bar(0)
    s2 = copy.deepcopy(s)
    for i in range(len(s)):  # 对每行用例进行匹配
        if (i % 100) == 0 or i == len(s) - 1:
            print_progress_bar(int(100 * i / (len(s) - 1)))
        t = 0
        for j in range(len(s[i])):  # 对每行用例的两两拆分进行判断，是否出现在其他行
            flag = False
            for i2 in [x for x in range(len(s2)) if s2[x] != s[i]]:  # 找同一列
                if s[i][j] == s2[i2][j]:
                    t = t + 1
                    flag = True
                    break
            if not flag:  # 同一列没找到，不用找剩余列了
                break
        if t == len(s[i]):
            del_row.append(i)
            s2.remove(s[i])
    res = [cp[i] for i in range(len(cp)) if i not in del_row]
    logger.info('过滤后:%s' % len(res))
    return res


# ---------------- 测试用例结束 ---------------------


# ---------------- 其他开始 ---------------------
try:
    import numpy as np
except ModuleNotFoundError:
    pass


class NpEncoder(json.JSONEncoder):
    """numpy类型转换"""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.int64):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.float64):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

# ---------------- 其他结束 ---------------------

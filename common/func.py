#!/usr/bin/python
# encoding=utf-8

"""
@Author : dongfanger
@Date   : 2019/12/12 10:58
@Desc   : common functions
"""

import ast
import base64
import csv
import datetime
import json
import os
import time

import numpy as np

from common.pytest_logger import logger, stdout_write


class NpEncoder(json.JSONEncoder):
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


def encrypt(pwd):
    """base64

    @param pwd: password
    @return: base64 password
    """
    return base64.b64encode(pwd.encode()).decode()


def current_time(t='time'):
    """time

    @param t: type: time/date/number
    @return: time
    """
    time_format = {'time': '%Y-%m-%d %H:%M:%S',
                   'date': '%Y-%m-%d',
                   'number': '%Y%m%d%H%M%S'}
    return time.strftime(time_format[t], time.localtime(time.time()))


def current_time_millis():
    """java time millis

    @return: Time millis
    """
    return int(time.time() * 1000)


def last_natural_day():
    """last natural day

    @return: last natural day
    """
    return (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")


def obj2json(x):
    """obj to json

    @param x: object eg:dict/str
    @return: json
    """
    if isinstance(x, dict):
        return json.dumps(x, ensure_ascii=False, cls=NpEncoder)
    elif isinstance(x, str):
        return ast.literal_eval(x.replace('null', '\'\'').replace('false', '\'\''))


def lower_id_uri(s):
    """string 'report/downExcel' to 'report_down_excel'

    @param s: upper
    @return: lower
    """
    s = ''.join(['_' + c.lower() if c.isupper()
                 else c for c in s.replace('/', '_')])
    return s[1:] if s[0] == '_' else s


def upper_id_uri(s):
    """string 'national_market_index' to 'NationalMarketIndex'

    @param s: lower
    @return: upper
    """
    return ''.join(x[0].upper() + x[1:] for x in s.replace(' ', '').replace('/', '_').split('_'))


def bar(i):
    """processing bar

    @param i: percent
    """
    c = int(i / 10)
    jd = '\r %2d%% [%s%s]'
    a = '■' * c
    b = '□' * (10 - c)
    stdout_write(jd % (i, a, b))


def json2form(body):
    """json to form

    @param body: {"a": 1, "b": 2}
    @return: a=1&b=2
    """
    return '&'.join([f"{k}={v}" for k, v in body.items()])


def form2json(form):
    """form to json

    @param form: a=1&b=2
    @return: {"a": 1, "b": 2}
    """
    body = {}
    for kv in form.split('&'):
        k, v = kv.split('=')
        body[k] = v
    return json.dumps(body, indent=4, ensure_ascii=False)


def print_column(select_result, cols):
    """after select, print specified cols

    @param select_result: sql select Result
    @param cols: cols to print
    """
    s = ''
    for c in cols:
        s += f'{c}: {select_result[c]}\n'
    logger.info(s)


def report_csv(path, title, row):
    """csv formatted test report of interface called info

    @param path: file path
    @param title: table title
    @param row: row
    """
    with open(path, 'a') as f:
        w = csv.writer(f)
        # If file is empty
        if not os.path.getsize(path):
            w.writerow(title)
        w.writerow(row)
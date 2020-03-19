#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   : 2019/12/12 10:58
@Desc   : Common functions
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
    """Base64

    @param pwd: Password
    @return: Base64 password
    """
    return base64.b64encode(pwd.encode()).decode()


def current_time(t='time'):
    """Time

    @param t: type: time/date/number
    @return: Time
    """
    time_format = {'time': '%Y-%m-%d %H:%M:%S',
                   'date': '%Y-%m-%d',
                   'number': '%Y%m%d%H%M%S'}
    return time.strftime(time_format[t], time.localtime(time.time()))


def current_time_millis():
    """Java time millis

    @return: Time millis
    """
    return int(time.time() * 1000)


def last_natural_day():
    """Last Natural day

    @return: Last Natural day
    """
    return (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")


def obj2json(x):
    """obj to json

    @param x: Object eg:dict/str
    @return: Json
    """
    if isinstance(x, dict):
        return json.dumps(x, ensure_ascii=False, cls=NpEncoder)
    elif isinstance(x, str):
        return ast.literal_eval(x.replace('null', '\'\'').replace('false', '\'\''))


def lower_id_uri(s):
    """String 'report/downExcel' to 'report_down_excel'

    @param s: Upper
    @return: Lower
    """
    s = ''.join(['_' + c.lower() if c.isupper()
                 else c for c in s.replace('/', '_')])
    return s[1:] if s[0] == '_' else s


def upper_id_uri(s):
    """String 'national_market_index' to 'NationalMarketIndex'

    @param s: Lower
    @return: Upper
    """
    return ''.join(x[0].upper() + x[1:] for x in s.replace(' ', '').replace('/', '_').split('_'))


def bar(i):
    """Processing bar

    @param i: percent
    """
    c = int(i / 10)
    jd = '\r %2d%% [%s%s]'
    a = '■' * c
    b = '□' * (10 - c)
    stdout_write(jd % (i, a, b))


def json2form(body):
    """Json to form

    @param body: {"a": 1, "b": 2}
    @return: a=1&b=2
    """
    return '&'.join([f"{k}={v}" for k, v in body.items()])


def form2json(form):
    """Form to json

    @param form: a=1&b=2
    @return: {"a": 1, "b": 2}
    """
    body = {}
    for kv in form.split('&'):
        k, v = kv.split('=')
        body[k] = v
    return json.dumps(body, indent=4, ensure_ascii=False)


def print_column(select_result, cols):
    """After select, print specified cols

    @param select_result: Sql select Result
    @param cols: Cols to print
    """
    s = ''
    for c in cols:
        s += f'{c}: {select_result[c]}\n'
    logger.info(s)


def report_csv(path, title, row):
    """Csv formatted test report of interface called info

    @param path: File path
    @param title: Table title
    @param row: Row
    """
    with open(path, 'a') as f:
        w = csv.writer(f)
        # If file is empty
        if not os.path.getsize(path):
            w.writerow(title)
        w.writerow(row)
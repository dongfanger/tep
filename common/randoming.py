"""
@Author : dongfanger
@Date   : 2019/12/12 10:58
@Desc   : random data
"""

import random
import time

from data.cache import chinese


def safe_sample(seq, n):
    """avoid list out of bound

    @param seq: sequence
    @param n: number
    @return: sample result
    """
    return random.sample(seq, n if n < len(seq) else len(seq))


def random_chinese(n):
    """random chinese

    @param n: number
    @return: sample result
    """
    return ''.join(random.sample(chinese.replace('\r', '').replace('\n', ''), n))


def random_id(n):
    """random id

    @param n: number
    @return: int sequence
    """
    s = ""
    for i in range(n):
        s += str(random.randint(0, 9))
    return int(s)


def random_01(n):
    """random 01 sequence

    @param n: number
    @return: code like '1010100'
    """
    return ''.join([random.choice('01') for i in range(n)])


def _timestamp(t):
    """timestamp

    @param t: time
    @return: timestamp
    """
    y, m, d = tuple(int(x) for x in t.split('-'))
    m = (y, m, d, 0, 0, 0, 0, 0, 0)
    return time.mktime(m)


def random_date(start, end, n):
    """random date

    @param start: start date
    @param end: end date
    @param n: number
    @return: random n date
    """
    start = _timestamp(start)
    end = _timestamp(end)
    return [time.strftime("%Y-%m-%d", time.localtime(random.randint(start, end))) for i in range(n)]


def range_num(a, b, interval=1.0):
    """range number

    @param a: start number
    @param b: end number
    @param interval: interval
    @return: number list
    """
    if interval == 1:
        return [i for i in range(a, b)]
    if interval == 0.5:
        out = []
        for i in range(a, b):
            out.append(i)
            out.append(i + 0.5)
        return out


def range_char(a, b, n=None):
    """range character list

    @param a: start number
    @param b: end number
    @param n: number
    @return: character list
    """
    out = [str(i) for i in range(a, b)]
    return out if n is None else safe_sample(out, n)

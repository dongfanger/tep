"""
@Author : Dongfanger
@Date   : 2019/12/12 10:58
@Desc   : Random data
"""

import random
import time

from data.cache import chinese


def safe_sample(seq, n):
    """Avoid list out of bound

    @param seq: Sequence
    @param n: Number
    @return: Sample result
    """
    return random.sample(seq, n if n < len(seq) else len(seq))


def random_chinese(n):
    """Random chinese

    @param n: Number
    @return: Sample result
    """
    return ''.join(random.sample(chinese.replace('\r', '').replace('\n', ''), n))


def random_id(n):
    """Random id

    @param n: Number
    @return: Int sequence
    """
    s = ""
    for i in range(n):
        s += str(random.randint(0, 9))
    return int(s)


def random_01(n):
    """Random 01 sequence

    @param n: Number
    @return: Code like '1010100'
    """
    return ''.join([random.choice('01') for i in range(n)])


def _timestamp(t):
    """Timestamp

    @param t: Time
    @return: Timestamp
    """
    y, m, d = tuple(int(x) for x in t.split('-'))
    m = (y, m, d, 0, 0, 0, 0, 0, 0)
    return time.mktime(m)


def random_date(start, end, n):
    """Random date

    @param start: Start date
    @param end: End date
    @param n: Number
    @return: Random n date
    """
    start = _timestamp(start)
    end = _timestamp(end)
    return [time.strftime("%Y-%m-%d", time.localtime(random.randint(start, end))) for i in range(n)]


def range_num(a, b, interval=1.0):
    """Range number

    @param a: Start number
    @param b: End number
    @param interval: Interval
    @return: Number list
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
    """Range character list

    @param a: Start number
    @param b: End number
    @param n: Number
    @return: Character list
    """
    out = [str(i) for i in range(a, b)]
    return out if n is None else safe_sample(out, n)

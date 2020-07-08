#!/usr/bin/python
# encoding=utf-8

"""
@Author : dongfanger
@Date   : 2019/12/12 10:58
@Desc   : algorithm to filter pairwise
"""

import copy
import decimal
import itertools

from common.func import bar
from common.pytest_logger import logger
from common.randoming import *
from pytest_allure import pare_wise_mode


def parewise(body):
    """parewise invoke function

    @param body: request body
    @return: body list filtered by parewise
    """
    start = time.process_time()

    my_body = copy.deepcopy(body)
    k = my_body.keys()
    v = [list(x) if isinstance(x, tuple) else [x] for x in my_body.values()]
    your_body = [dict(zip(k, combination)) for combination in _filter_combination(v)]

    end = time.process_time()
    elapsed = decimal.Decimal("%.2f" % float(end - start))
    logger.info(' filtered:%s elapsed:%ss' % (len(your_body), elapsed))
    # choose 1 record random for regression, lower cover degree, but improve efficiency
    return your_body if pare_wise_mode == 1 else safe_sample(your_body, 1)


def _filter_combination(option):
    """filter to get pare combinations

    @param option: [['M', 'O', 'P'], ['W', 'L', 'I'], ['O', 'W', 'K'], ['A', 'B', 'C']]
    @return:[('M', 'W', 'K', 'C'), ('M', 'L', 'K', 'C'), ('M', 'I', 'O', 'C'), ...]
    """
    #  Cartesian product
    cp = []
    # Pare
    pare = []
    for x in eval('itertools.product' + str(tuple(option))):
        cp.append(x)
        pare.append([i for i in itertools.combinations(x, 2)])
    logger.info('cartesian product rows:%s' % len(cp))

    del_row = []
    bar(0)
    pare2 = copy.deepcopy(pare)
    # match each row
    for i in range(len(pare)):
        if (i % 100) == 0 or i == len(pare) - 1:
            bar(int(100 * i / (len(pare) - 1)))
        t = 0
        # estimate pare of each row, if appeared in other rows
        for j in range(len(pare[i])):  # 对每行用例的两两拆分进行判断，是否出现在其他行
            flag = False
            for i2 in [x for x in range(len(pare2)) if pare2[x] != pare[i]]:  # 找同一列
                if pare[i][j] == pare2[i2][j]:
                    t += 1
                    flag = True
                    break
            # one column not found, no need to find other columns
            if not flag:
                break
        if t == len(pare[i]):
            del_row.append(i)
            pare2.remove(pare[i])
    return [cp[i] for i in range(len(cp)) if i not in del_row]


def checkbox(option, t=0, j=None):
    """checkbox transfer

    @param option: [1, 2, 3]
    @param t: option type, 0:list 1:str
    @param j: string connector, eg:the j of '1, 2, 3' is comma
    @return: [1, 2, 3], [random_option]
    """
    if isinstance(option, str):
        t = 1
        j = ',' if j is None else j
        option = option.split(',')
    random_option = safe_sample(option, random.randint(1, len(option) - 1))
    return (option, random_option) if t == 0 else (j.join(option), j.join(random_option))


def test():
    body = {1: ('M', 'O', 'P'),
            2: ('W', 'L', 'I'),
            3: ('O', 'W', 'K'),
            4: ('A', 'B', 'C')}
    a = parewise(body)
    for b in a:
        logger.info(b)

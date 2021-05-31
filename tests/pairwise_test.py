#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2021/05/30 15:11
@Desc    :  
"""
import itertools

from tep.func import pairwise, body_pair


# algorithm：if the pairwise combination result of a use case appears in other combinations,
# the use case is deleted to simplify the use case.


def test_cartesian_product():
    enum = [['M', 'O', 'P'], ['W', 'L', 'I'], ['C', 'E']]
    cp = []  # cartesian product
    pair = []  # pair
    for x in eval('itertools.product' + str(tuple(enum))):
        cp.append(x)
        pair.append([i for i in itertools.combinations(x, 2)])
    print()
    for x in cp:
        print(x)


def test_pairwise():
    enum = [['M', 'O', 'P'], ['W', 'L', 'I'], ['C', 'E']]
    result = pairwise(enum)
    print(f"\npair total:{len(result)}")
    for p in result:
        print(p)


def test_body_pair():
    body_enum = {
        "platform": ("windows", "linux", "macos"),
        "color": ("red", "blue", "yellow", "black", "white"),
        "position": ("left", "center", "right"),
        "id": (1, 2, 3, 4)
    }
    for pair in body_pair(body_enum):
        print(pair)

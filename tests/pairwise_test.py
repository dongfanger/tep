#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2021/05/30 15:11
@Desc    :  
"""
from tep.func import pairwise, body_pair


def test_pairwise():
    enum = [['M', 'O', 'P'], ['W', 'L', 'I'], ['O', 'W', 'K'], ['A', 'B', 'C']]
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

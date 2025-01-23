#!/usr/bin/python
# encoding=utf-8
from tep import json


def test_success():
    # raw string
    body = r"""
{
    "a": 1,
    "b": "{\"x\": 2}"
}      
"""
    json.loads(body)


def test_fail():
    body = """
{
    "a": 1,
    "b": "{\"x\": 2}"
}      
"""
    json.loads(body)

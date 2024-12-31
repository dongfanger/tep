#!/usr/bin/python
# encoding=utf-8
from tep import v


def test():
    v({
        "reason": "no"
    })
    test_json = """
{
  "username": "cekaigang",
  "password": "can not tell you"
  "reason": "${reason}"
}
"""
    print(v(test_json))


def test_repeat():
    v({
        "reason": "no"
    })
    test_json = """
{
  "username": "cekaigang",
  "password": "can not tell you"
  "why": "${reason}",
  "what": "${reason}",
  "how": "${reason}"
}
"""
    print(v(test_json))

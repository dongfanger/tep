#!/usr/bin/python
# encoding=utf-8
from tep import v


def test():
    v({
        'reason': 'no'
    })
    test_json = '''
{
  "username": "cekaigang",
  "password": "can not tell you"
  "reason": "${reason}"
}
'''
    print(v(test_json))


def test_repeat():
    v({
        "reason": "no"
    })
    test_json = '''
{
  "username": "cekaigang",
  "password": "can not tell you"
  "why": "${reason}",
  "what": "${reason}",
  "how": "${reason}"
}
'''
    print(v(test_json))


def test_none():
    print()
    print(v('msg'))  # msg
    print(v(key='msg'))  # None


def test_list():
    v({
        "a": [1, 2, 3]
    })
    print(v('a'))
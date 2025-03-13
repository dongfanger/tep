#!/usr/bin/python
# encoding=utf-8

from tep import file


def test():
    print(file('Cookie'))


def test_json():
    print(file('type', 'x.json'))


def test_yaml():
    print(file('type', 'y.yaml'))

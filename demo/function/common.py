#!/usr/bin/python
# encoding=utf-8
import os.path

from tep import file


def base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def headers():
    return {'Content-Type': 'application/json', 'Cookie': file(os.path.join(base_dir(), 'file', 'Cookie'))}

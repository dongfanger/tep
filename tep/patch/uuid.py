#!/usr/bin/python
# encoding=utf-8
import uuid as u


def uuid():
    return str(u.uuid1()).replace("-", "")

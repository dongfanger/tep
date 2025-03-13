#!/usr/bin/python
# encoding=utf-8
import uuid


def patch_uuid():
    return str(uuid.uuid1()).replace('-', '')

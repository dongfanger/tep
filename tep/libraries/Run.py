#!/usr/bin/python
# encoding=utf-8

import os

from tep.libraries.Config import Config
from tep.libraries.Cmd import Cmd


class Run:
    def __init__(self, *args, **kwargs):
        os.system(Cmd(*args).pytest())

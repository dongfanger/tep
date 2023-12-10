#!/usr/bin/python
# encoding=utf-8

import os

from tep.libraries.Config import Config
from tep.libraries.File import File


def UserDefinedVariablesImpl(*args, **kwargs):
    file_path = os.path.join(Config().DATA_DIR, "UserDefinedVariables.yaml")
    return File(file_path).load()

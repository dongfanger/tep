#!/usr/bin/python
# encoding=utf-8

import os

from tep.libraries.Config import Config
from tep.libraries.File import File
from tep.libraries.Result import Result


def UserDefinedVariablesImpl(*args, **kwargs) -> Result:
    file_path = os.path.join(Config().DATA_DIR, "UserDefinedVariables.yaml")
    result = Result()
    result.data = File(file_path).load()
    return result

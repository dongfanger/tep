#!/usr/bin/python
# encoding=utf-8

import os

from tep.libraries.Config import Config
from tep.libraries.File import File
from tep.libraries.Result import Result


def DataImpl(file_path: str) -> Result:
    file_path = os.path.join(Config().DATA_DIR, file_path)
    result = Result()
    result.data = File(file_path).load()
    return result

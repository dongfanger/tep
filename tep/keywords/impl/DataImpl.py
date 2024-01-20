#!/usr/bin/python
# encoding=utf-8

import os

from tep.libraries.Config import Config
from tep.libraries.File import File


def DataImpl(file_path: str):
    file_path = os.path.join(Config().DATA_DIR, file_path)
    return File(file_path).load()

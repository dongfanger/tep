#!/usr/bin/python
# encoding=utf-8
import json
import os.path

import yaml

from tep.config import Config


def file(*args):
    path = os.path.join(Config().FILE_DIR, *args)
    return _load(path)

def filepath():
    """
    Effective when using Pytest: from tep import filepath
    Otherwise: from function.common import base_dir
    """
    return Config().FILE_DIR


def _load(path):
    file_type = _file_type(path)
    if file_type in ['.yml', '.yaml', '.YML', 'YAML']:
        return _yaml_load(path)
    elif file_type in ['.json', '.JSON']:
        return _json_load(path)
    else:
        with open(path, encoding='utf8') as f:
            return f.read()


def _file_type(path) -> str:
    return os.path.splitext(path)[-1]


def _yaml_load(path) -> [dict, list]:
    with open(path, encoding='utf8') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def _json_load(path) -> [dict, list]:
    with open(path, encoding='utf8') as f:
        return json.load(f)

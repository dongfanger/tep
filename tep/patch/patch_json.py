#!/usr/bin/python
# encoding=utf-8
import inspect
import json
import jsonpath as jp
from tep.patch.patch_logging import logger


def simplify(json_str: str) -> str:
    json_dict = loads(json_str)
    return json.dumps(json_dict, separators=(',', ':'), ensure_ascii=False)


def beautify(json_str: str, indent: int = 4) -> str:
    json_dict = loads(json_str)
    return json.dumps(json_dict, separators=(',', ':'), indent=indent, ensure_ascii=False)


def escape(json_str: str) -> str:
    return json.dumps(json_str, ensure_ascii=False)[1:-1]


def loads(json_str: str) -> dict:
    json_dict = {}
    try:
        json_dict = json.loads(json_str)
    except:
        caller_code = inspect.currentframe().f_back.f_code
        logger.error(f'{caller_code.co_filename}::{caller_code.co_name} error, parse json str exception:\n{json_str} ')
    return json_dict


def dumps(json_dict) -> str:
    return json.dumps(json_dict, ensure_ascii=False)


def parse(json_str):
    return loads(json_str)


def to_json_string(json_dict) -> str:
    return dumps(json_dict)


def json2sql(json_dict: dict, table_name: str) -> str:
    fields = list()
    values = list()
    for key, value in json_dict.items():
        fields.append(key)
        if value is None:
            value = 'null'
        else:
            if '"' in value:
                value = escape(value)
            value = "'" + value + "'"
        values.append(value)
    return f'insert into {table_name}({",".join(fields)}) values ({",".join(values)});'


def jsonpath(json_dict, expr):
    data = jp.jsonpath(json_dict, expr)
    if not data:
        return None
    if isinstance(data, list) and len(data) == 1:
        return data[0]
    return data
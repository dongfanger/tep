#!/usr/bin/python
# encoding=utf-8
import inspect
import json
import logging


def simplify(json_str: str) -> str:
    json_dict = loads(json_str)
    return json.dumps(json_dict, separators=(',', ':'), ensure_ascii=False)


def beautify(json_str: str, indent: int = 4) -> str:
    json_dict = loads(json_str)
    return json.dumps(json_dict, separators=(',', ':'), indent=indent, ensure_ascii=False)


def nested(json_str: str) -> str:
    json_dict = loads(json_str)

    return json.dumps(json_dict, separators=(',', ':'), ensure_ascii=False).replace('"', '\\"')


def loads(json_str: str) -> dict:
    json_dict = {}
    try:
        json_dict = json.loads(json_str)
    except:
        caller_code = inspect.currentframe().f_back.f_code
        logging.error(f"{caller_code.co_filename}::{caller_code.co_name} error, string is not json format:\n{json_str} ")

    return json_dict


def dumps(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False)


def json2sql(json_dict: dict, table_name: str) -> str:
    fields = list()
    values = list()
    for key, value in json_dict.items():
        fields.append(key)
        if value is None:
            value = "null"
        else:
            if '"' in value:
                value = nested(value)
            value = '"' + value + '"'

        values.append(value)
    return f"insert into {table_name}({','.join(fields)}) values ({','.join(values)});"

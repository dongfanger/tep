#!/usr/bin/python
# encoding=utf-8
import inspect
import json as j
import logging


def simplify(json_str: str) -> str:
    json_dict = loads(json_str)
    return j.dumps(json_dict, separators=(',', ':'), ensure_ascii=False)


def beautify(json_str: str, indent: int = 4) -> str:
    json_dict = loads(json_str)
    return j.dumps(json_dict, separators=(',', ':'), indent=indent, ensure_ascii=False)


def nested(json_str: str) -> str:
    json_dict = loads(json_str)

    return j.dumps(json_dict, separators=(',', ':'), ensure_ascii=False).replace('"', '\\"')


def loads(json_str: str) -> dict:
    json_dict = {}
    try:
        json_dict = j.loads(json_str)
    except:
        caller_code = inspect.currentframe().f_back.f_code
        logging.error(f"{caller_code.co_filename}::{caller_code.co_name} error, string is not json format:\n{json_str} ")

    return json_dict


def dumps(data: dict) -> str:
    return j.dumps(data, ensure_ascii=False)

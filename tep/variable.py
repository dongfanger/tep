#!/usr/bin/python
# encoding=utf-8
import json
import re


def v(*args, **kwargs):
    if len(args) == 1:
        if isinstance(args[0], dict):
            _init(args[0])
        elif isinstance(args[0], str):
            return _parse(args[0])
    elif len(args) == 2:
        _set(args[0], args[1])


class TepVar:
    kv = {}


class Constant:
    JSON = "json"
    STR = "str"


def _init(kv: dict):
    TepVar.kv = kv


def _set(key, value):
    TepVar.kv[key] = value


def _parse(data: str):
    data = data.strip()
    if Constant.STR == _str_parsed_type(data):
        return _parse_str(data)
    elif Constant.JSON == _str_parsed_type(data):
        return _parse_json(data)


def _str_parsed_type(data: str):
    if data.startswith("{"):
        return Constant.JSON
    else:
        return Constant.STR


def _parse_str(data: str) -> str:
    new_str = _replace_var(data)
    if new_str:
        return new_str
    return data


def _parse_json(data: str) -> dict:
    new_str = _replace_var(data)
    if new_str:
        return json.loads(new_str)

    return json.loads(data)


def _replace_var(str_param: str) -> str:
    var_list = _parse_var(str_param)
    if var_list:
        str_param = str_param.replace('{', '{{').replace('}', '}}')
        kv = TepVar.kv
        for var in var_list:
            start_index = str_param.find('${{' + var + '}}')
            end_index = start_index + len(var) + 5  # Length of ${{}}
            dollar_var = str_param[start_index: end_index]
            str_param = str_param.replace(dollar_var, '{' + var + '}')
            if var not in kv:
                kv[var] = "null"
        return str_param.format(**kv)
    return ""


def _parse_var(json_str: str) -> list:
    json_str = json_str.replace('{', '{{').replace('}', '}}')
    pattern = r'\${{([^}]+)}}'
    matches = re.findall(pattern, json_str)
    return matches

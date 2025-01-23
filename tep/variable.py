#!/usr/bin/python
# encoding=utf-8
import inspect
import logging
import re

from tep.patch.patch_random import patch_random
from tep.patch.patch_time import patch_time, timestamp
from tep.patch.patch_uuid import patch_uuid


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
    build_in_functions = [
        "random",
        "uuid",
        "time",
        "timestamp"
    ]


def _init(kv: dict):
    TepVar.kv = kv


def _set(key, value):
    TepVar.kv[key] = value


def _get(key):
    return TepVar.kv[key]


def _parse(data: str) -> str:
    data = data.strip()
    if data in TepVar.kv:
        return _get(data)
    else:
        new_str = _replace_var(data)
        return new_str if new_str else data


def _replace_var(str_param: str) -> str:
    var_list = _parse_var(str_param)
    if var_list:
        str_param = str_param.replace('{', '{{').replace('}', '}}')
        kv = TepVar.kv
        for var in var_list:
            start_index = str_param.find('${{' + var + '}}')
            end_index = start_index + len(var) + 5  # Length of ${{}}
            dollar_var = str_param[start_index: end_index]

            function_name, parameters = _parse_function(var)
            if not function_name and var not in kv:
                kv[var] = None
                logging.warning(f'Can not find variable {var} in TepVar.kv, default None')
                continue

            if function_name:
                if function_name not in TepVar.build_in_functions:
                    logging.warning(f'Can not find function {function_name} in built-in functions')

                kv[function_name] = _call_function(function_name, parameters)

            variable_name = function_name if function_name else var
            str_param = str_param.replace(dollar_var, '{' + variable_name + '}')

        return str_param.format(**kv)

    return ''


def _parse_var(json_str: str) -> set:
    json_str = json_str.replace('{', '{{').replace('}', '}}')
    pattern = r'\${{([^}]+)}}'
    matches = re.findall(pattern, json_str)
    return set(matches)


def _parse_function(s):
    pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*$'
    match = re.match(pattern, s)
    if match:
        function_name = match.group(1)
        parameters = match.group(2)
        parameters = [param.strip() for param in parameters.split(',')] if parameters else []
        return function_name, parameters
    else:
        return None, None


def _call_function(function_name, parameters):
    try:
        if function_name == "random":
            return patch_random(*parameters)
        elif function_name == "uuid":
            return patch_uuid()
        elif function_name == "time":
            return patch_time(*parameters)
        elif function_name == "timestamp":
            return timestamp(*parameters)
    except:
        caller_code = inspect.currentframe().f_back.f_code
        logging.error(f"{caller_code.co_filename}::{caller_code.co_name} function {function_name} error, return -1")
        return -1

#!/usr/bin/python
# encoding=utf-8
import inspect
import re
from typing import Optional

from tep.patch.patch_random import patch_random
from tep.patch.patch_time import patch_time, timestamp
from tep.patch.patch_uuid import patch_uuid
from tep.patch.patch_logging import logger


def v(*args, **kwargs):
    if 'key' in kwargs:
        return _get(kwargs['key'])

    if len(args) == 1:
        if isinstance(args[0], dict):
            _batch(args[0])
        elif isinstance(args[0], str):
            return _parse(args[0])
    elif len(args) == 2:
        _set(args[0], args[1])


class TepVar:
    kv = {}
    build_in_functions = [
        'random',
        'uuid',
        'time',
        'timestamp'
    ]


def _batch(kv: dict):
    for key, value in kv.items():
        _set(key, value)


def _set(key, value):
    if isinstance(value, str):
        value = _replace_var(value)
    TepVar.kv[key] = value


def _get(key):
    return TepVar.kv.get(key, None)


def _parse(data: str) -> Optional[str]:
    value = _get(data)
    if value is not None:
        if isinstance(value, str):
            return _replace_var(value)
        return value

    return _replace_var(data)


def _replace_var(data: str) -> str:
    var_list = _parse_var(data)
    if var_list:
        data = data.replace('{', '{{').replace('}', '}}')
        kv = TepVar.kv
        for var in var_list:
            start_index = data.find('${{' + var + '}}')
            end_index = start_index + len(var) + 5  # Length of ${{}}
            dollar_var = data[start_index: end_index]

            function_name, parameters = _parse_function(var)
            if function_name:
                if function_name not in TepVar.build_in_functions:
                    logger.warning(f'Can not find function {function_name} in built-in functions')

                kv[function_name] = _call_function(function_name, parameters)
            else:
                if var not in kv:
                    # Can not find var in TepVar.kv, default None
                    kv[var] = None
                    continue
                value = kv[var]
                if isinstance(value, str):
                    kv[var] = _replace_var(value)
            variable_name = function_name if function_name else var
            data = data.replace(dollar_var, '{' + variable_name + '}')
        return data.format(**kv)

    return data


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
        if function_name == 'random':
            return patch_random(*parameters)
        elif function_name == 'uuid':
            return patch_uuid()
        elif function_name == 'time':
            return patch_time(*parameters)
        elif function_name == 'timestamp':
            return timestamp(*parameters)
    except:
        caller_code = inspect.currentframe().f_back.f_code
        logger.error(f'{caller_code.co_filename}::{caller_code.co_name} function {function_name} error, return -1')
        return -1

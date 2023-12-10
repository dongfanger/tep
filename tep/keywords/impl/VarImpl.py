#!/usr/bin/python
# encoding=utf-8
import re


class CaseVar:
    var = None


def VarImpl(var: dict = None):
    if var:
        CaseVar.var = var
    return CaseVar.var


def replace_var(str_param: str) -> str:
    var_list = _parse_var(str_param)
    if var_list:
        str_param = str_param.replace('{', '{{').replace('}', '}}')
        case_var = CaseVar.var
        for var in var_list:
            start_index = str_param.find('${{' + var + '}}')
            end_index = start_index + len(var) + 5  # 加上${{}}的长度
            dollar_var = str_param[start_index: end_index]
            str_param = str_param.replace(dollar_var, '{' + var + '}')
            if var not in case_var:
                case_var[var] = "null"
        return str_param.format(**case_var)
    return ""


def _parse_var(json_str: str) -> list:
    json_str = json_str.replace('{', '{{').replace('}', '}}')
    pattern = r'\${{([^}]+)}}'
    matches = re.findall(pattern, json_str)
    return matches

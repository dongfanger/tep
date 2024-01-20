#!/usr/bin/python
# encoding=utf-8

from tep.keywords.impl.VarImpl import replace_var


def StringImpl(str_param: str) -> str:
    new_str = replace_var(str_param)
    if new_str:
        return new_str
    return str_param

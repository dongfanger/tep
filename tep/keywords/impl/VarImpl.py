#!/usr/bin/python
# encoding=utf-8

class CaseVar:
    var = None


def VarImpl(var: dict = None):
    if var:
        CaseVar.var = var
    return CaseVar.var

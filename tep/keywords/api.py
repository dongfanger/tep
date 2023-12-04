import pytest

from tep.keywords.impl.JSONImpl import JSONImpl
from tep.keywords.impl.DataImpl import DataImpl
from tep.keywords.impl.DbcImpl import DbcImpl
from tep.keywords.impl.HTTPRequestImpl import HTTPRequestImpl
from tep.keywords.impl.UserDefinedVariablesImpl import UserDefinedVariablesImpl
from tep.keywords.impl.VarImpl import VarImpl
from tep.libraries.Args import Args

"""
Adaptation Layer, accept any parameter, return Result object，backward compatible
"""


@pytest.fixture(scope="session")
def HTTPRequestKeyword():
    def _function(*args, **kwargs):
        method, url, kwargs = Args.parse(["method", "url"], args, kwargs)
        return HTTPRequestImpl(method, url, **kwargs)

    return _function


@pytest.fixture(scope="session")
def JSONKeyword():
    def _function(*args, **kwargs):
        try:
            json_str, expr, kwargs = Args.parse(["json_str", "expr"], args, kwargs)
        except Exception:
            json_str, kwargs = Args.parse(["json_str", "expr"], args, kwargs)
            expr = None
        return JSONImpl(json_str, expr)

    return _function


@pytest.fixture(scope="session")
def UserDefinedVariablesKeyword():
    def _function(*args, **kwargs):
        return UserDefinedVariablesImpl()

    return _function


@pytest.fixture(scope="session")
def DataKeyword():
    def _function(*args, **kwargs):
        file_path, kwargs = Args.parse(["file_path"], args, kwargs)
        return DataImpl(file_path)

    return _function


@pytest.fixture(scope="session")
def DbcKeyword():
    def _function(*args, **kwargs):
        host, port, user, password, database, kwargs = Args.parse(["host", "port", "user", "password", "database"], args, kwargs)
        return DbcImpl(host, port, user, password, database)

    return _function


@pytest.fixture(scope="session")
def VarKeyword():
    def _function(*args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return VarImpl()
        var, kwargs = Args.parse(["var"], args, kwargs)
        return VarImpl(var)

    return _function

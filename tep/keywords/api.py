import pytest

from tep.keywords.impl.DataImpl import DataImpl
from tep.keywords.impl.DbcImpl import DbcImpl
from tep.keywords.impl.HTTPRequestImpl import HTTPRequestImpl
from tep.keywords.impl.JSONImpl import JSONImpl
from tep.keywords.impl.StringImpl import StringImpl
from tep.keywords.impl.UserDefinedVariablesImpl import UserDefinedVariablesImpl
from tep.keywords.impl.VarImpl import VarImpl

"""
Adaptation Layer, accept any parameter, return Result object，backward compatible
"""


@pytest.fixture(scope="session")
def HTTPRequestKeyword():
    def _function(method, url, **kwargs):
        return HTTPRequestImpl(method, url, **kwargs)

    return _function


@pytest.fixture(scope="session")
def JSONKeyword():
    def _function(json_str, **kwargs):
        return JSONImpl(json_str, **kwargs)

    return _function


@pytest.fixture(scope="session")
def StringKeyword():
    def _function(str_param, **kwargs):
        return StringImpl(str_param, **kwargs)

    return _function


@pytest.fixture(scope="session")
def UserDefinedVariablesKeyword():
    def _function(**kwargs):
        return UserDefinedVariablesImpl(**kwargs)

    return _function


@pytest.fixture(scope="session")
def DataKeyword():
    def _function(file_path, **kwargs):
        return DataImpl(file_path, **kwargs)

    return _function


@pytest.fixture(scope="session")
def DbcKeyword():
    def _function(host, port, user, password, database, **kwargs):
        return DbcImpl(host, port, user, password, database, **kwargs)

    return _function


@pytest.fixture(scope="session")
def VarKeyword():
    def _function(var=None, **kwargs):
        return VarImpl(var, **kwargs)

    return _function

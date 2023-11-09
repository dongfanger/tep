import pytest

from tep.keywords.impl.BodyImpl import BodyImpl
from tep.keywords.impl.DataImpl import DataImpl
from tep.keywords.impl.DbcImpl import DbcImpl
from tep.keywords.impl.HTTPRequestImpl import HTTPRequestImpl
from tep.keywords.impl.UserDefinedVariablesImpl import UserDefinedVariablesImpl
from tep.libraries.Args import Args
from tep.libraries.Result import Result

"""
Adaptation Layer, accept any parameter, return Result object，backward compatible
"""


@pytest.fixture(scope="session")
def HTTPRequestKeyword():
    def _function(*args, **kwargs) -> Result:
        method, url, kwargs = Args.parse(["method", "url"], args, kwargs)
        return HTTPRequestImpl(method, url, **kwargs)

    return _function


@pytest.fixture(scope="session")
def BodyKeyword():
    def _function(*args, **kwargs) -> Result:
        json_str, expr, kwargs = Args.parse(["json_str", "expr"], args, kwargs)
        return BodyImpl(json_str, expr)

    return _function


@pytest.fixture(scope="session")
def UserDefinedVariablesKeyword():
    def _function(*args, **kwargs) -> Result:
        return UserDefinedVariablesImpl()

    return _function


@pytest.fixture(scope="session")
def DataKeyword():
    def _function(*args, **kwargs) -> Result:
        file_path, kwargs = Args.parse(["file_path"], args, kwargs)
        return DataImpl(file_path)

    return _function


@pytest.fixture(scope="session")
def DbcKeyword():
    def _function(*args, **kwargs) -> Result:
        host, port, user, password, database, kwargs = Args.parse(["host", "port", "user", "password", "database"], args, kwargs)
        return DbcImpl(host, port, user, password, database)

    return _function

import pytest

from tep.plugin import tep_plugins

pytest_plugins = tep_plugins()


def hello():
    return 100

@pytest.fixture
def other_fixture():
    print("我先执行")

@pytest.fixture
def nest(other_fixture):
    def func(message):
        return message
    return func


def test_nest(nest):
    print(nest("晚上好"))


@pytest.fixture
def hello_fixture():
    def func_name():
        print("我是fixture内部函数")
        return 100
    return func_name

def test_func(hello_fixture):
    # print(type(hello_fixture))
    score = hello_fixture()  # func_name()
    print(score)


if __name__ == '__main__':
    score = hello()
    print(score)
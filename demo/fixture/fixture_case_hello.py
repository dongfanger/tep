#!/usr/bin/python
# encoding=utf-8

import pytest
from tep import v


@pytest.fixture(scope='session')
def case_hello():
    def main():
        msg = 'Hello ${name}'
        msg = v(msg)
        print(msg)

    return main

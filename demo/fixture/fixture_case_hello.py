#!/usr/bin/python
# encoding=utf-8

import pytest
from tep import v, logger


@pytest.fixture(scope='session')
def case_hello():
    def main():
        msg = 'Hello ${name}'
        msg = v(msg)
        logger.info(msg)
    return main

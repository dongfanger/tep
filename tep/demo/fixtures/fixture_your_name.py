#!/usr/bin/python
# encoding=utf-8

""" Please define your own fixture.
"""

from tep.fixture import *


@pytest.fixture(scope="session")
def env_vars_your_name(config):
    class Clazz:
        env = config["env"]

        # Environment and variables
        mapping = {
            "qa": {
                "your_var": "123",
            },
            "release": {
                "your_var": "456",
            }
            # Add your environment and variables
        }
        # Define properties for auto display
        your_var = mapping[env]["your_var"]

    return Clazz()


@pytest.fixture
def share_your_name():
    pass

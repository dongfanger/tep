#!/usr/bin/python
# encoding=utf-8

""" Can only be modified by the administrator. Only fixtures are provided.
"""

import os

import pytest
import yaml

# Initial
_project_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session", autouse=True)
def project_cache(request):
    request.config.cache.set("project_dir", _project_dir)


@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(_project_dir, "conf.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        conf = yaml.load(f.read(), Loader=yaml.FullLoader)
        return conf


@pytest.fixture(scope="session")
def files_dir():
    return os.path.join(_project_dir, "files")


# Import fixtures
exec("from fixtures.fixture_admin import *")
exec("from fixtures.fixture_your_name import *")

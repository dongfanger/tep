#!/usr/bin/python
# encoding=utf-8

""" Can only be modified by the administrator. Only fixtures are provided.
"""

import os

import pytest

# Initial
_project_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session", autouse=True)
def _project_cache(request):
    request.config.cache.set("project_dir", _project_dir)


@pytest.fixture(scope="session", autouse=True)
def _automatic_import_fixtures(_project_cache):
    fixtures_dir = os.path.join(_project_dir, "fixtures")
    for root, _, files in os.walk(fixtures_dir):
        for file in files:
            if os.path.isfile(os.path.join(root, file)):
                if file.startswith("fixture_") and file.endswith(".py"):
                    fixture_name, _ = os.path.splitext(file)
                    exec(f"from fixtures.{fixture_name} import *")

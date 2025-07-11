#!/usr/bin/python
# encoding=utf-8
import inspect
import os
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

from tep.config import Config


def tep_plugins():
    """
    Must be placed at the top, execute first to initialize base dir
    """
    caller = inspect.stack()[1]
    Config.BASE_DIR = os.path.abspath(os.path.dirname(caller.filename))
    plugins = _fixture_path()  # +[other plugins]
    return plugins


def _fixture_path():
    _fixture_dir = Config().FIXTURE_DIR
    paths = []
    # project/fixtures
    for root, _, files in os.walk(_fixture_dir):
        for file in files:
            if file.startswith('fixture_') and file.endswith('.py'):
                full_path = os.path.join(root, file)
                import_path = full_path.replace(_fixture_dir, '').replace('\\', '.')
                import_path = import_path.replace('/', '.').replace('.py', '')
                paths.append('fixture' + import_path)
    return paths


def _tep_read_template(search_paths, template_name='index2.jinja2'):
    env = Environment(
        loader=FileSystemLoader(search_paths),
        autoescape=select_autoescape(
            enabled_extensions=('jinja2',),
        ),
    )
    return env.get_template(template_name)


class Plugin:
    @staticmethod
    def pytest_html_report_title(report):
        report.title = 'TepReport'

    @staticmethod
    def pytest_configure(config):
        import pytest_html
        resources_dir = os.path.join(os.path.dirname(os.path.abspath(pytest_html.__file__)), 'resources')
        tep_resources_dir = os.path.join(Config.TEP_DIR, 'resources')
        shutil.copytree(tep_resources_dir, resources_dir, dirs_exist_ok=True)

#!/usr/bin/python
# encoding=utf-8

import os

from tep.config import Config


def run(settings: dict):
    template = 'pytest -s {path} {tep_report}'
    paths = [str(os.path.join(Config().TESTS_DIR, x)) for x in settings['path']]
    cmd = template.format(
        path=' '.join(paths),
        tep_report=_tep_report(settings['report'])
    )
    os.system(cmd)


def _tep_report(report: bool):
    if report:
        return f'--html={Config().HTML_REPORT_PATH}.html --self-contained-html'
    return ''

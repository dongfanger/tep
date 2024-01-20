#!/usr/bin/python
# encoding=utf-8
import os.path

from tep.libraries.Config import Config


class Cmd:
    template = "pytest {where_to_run} {tep_report}"

    def __init__(self, *args, **kwargs):
        settings = args[0]
        self.RUN_PATH = [os.path.join(Config().CASE_DIR, path) for path in settings["path"]]
        self.RUN_REPORT = settings["report"]

    def pytest(self) -> str:
        cmd = self.template.format(
            where_to_run=" ".join(self.RUN_PATH),
            tep_report=self.tep_report()
        )
        return cmd

    def tep_report(self) -> str:
        if self.RUN_REPORT:
            return f"--html={Config().HTML_REPORT_PATH}.html --self-contained-html"
        return ""

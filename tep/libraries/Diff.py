import difflib
import json
import os
import time

from deepdiff import DeepDiff

from tep.libraries.Sqlite import Sqlite


class Diff:
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    DIFF_TXT_FILE = "{}.txt".format(current_time)
    DIFF_HTML_FILE = "{}.html".format(current_time)

    @staticmethod
    def make(case_id: str, diff_dir: str):
        results = Sqlite.get_expect_actual(case_id)
        diffs = []
        expect_text = ""
        actual_text = ""
        for row in results:
            expect, actual, method, url = row
            diff = Diff.make_deepdiff(expect, actual)
            diffs.append(diff)
            expect_text += Diff._format_json_str(expect, method, url)
            actual_text += Diff._format_json_str(actual, method, url)
        diff_html = Diff.make_difflib(expect_text, actual_text)
        Diff._output_file(diffs, diff_html, diff_dir)

    @staticmethod
    def make_deepdiff(expect: str, actual: str) -> str:
        diff = DeepDiff(expect, actual)
        return str(diff)

    @staticmethod
    def make_difflib(lines1: str, lines2: str) -> str:
        diff = difflib.HtmlDiff().make_file(lines1.splitlines(), lines2.splitlines())
        return diff

    @staticmethod
    def _format_json_str(text: str, method: str, url: str) -> str:
        s = json.dumps(json.loads(text), indent=4, ensure_ascii=False)
        s = "{} {}\n{}\n\n".format(method, url, s)
        return s

    @staticmethod
    def _output_file(diffs: list, diff_html: str, diff_dir: str):
        with open(os.path.join(diff_dir, Diff.DIFF_TXT_FILE), "w") as f:
            f.write("\n\n".join(diffs))

        styled_html = f"<style>td {{width: 50%;}}</style>\n{diff_html}"
        with open(os.path.join(diff_dir, Diff.DIFF_HTML_FILE), "w") as f:
            f.write(styled_html)

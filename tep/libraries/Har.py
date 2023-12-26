import base64
import json
import os
import uuid

from haralyzer import HarParser
import logging

from tep.libraries.JSON import JSON
from tep.libraries.Profile import Profile
from tep.libraries.Sqlite import Sqlite
from tep.libraries.Step import Step


class Har:
    TEMPLATE = """def test(HTTPRequestKeyword, VarKeyword, StringKeyword, JSONKeyword):
    var = VarKeyword({var})
    {steps}
"""

    TEMPLATE_IMPORT_REPLAY = """from tep.libraries.Diff import Diff
from tep.libraries.Sqlite import Sqlite


"""

    TEMPLATE_DIFF = """
    Diff.make(var["caseId"], var["diffDir"])
"""

    def __init__(self, profile: dict):
        self.profile = Profile()
        self.profile.har_file = profile.get("harFile", "")
        self.profile.har_dir = profile.get("harDir", "")
        self.profile.des_dir = profile.get("desDir", "")
        self.profile.overwrite = profile.get("overwrite", False)
        self.profile.replay = profile.get("replay", False)
        self.profile.json_indent = profile.get("jsonIndent", 4)
        self.profile.http2 = profile.get("http2", False)
        self.profile.hook_var = profile.get("hookVar", {})
        self.profile.hook_url = profile.get("hookUrl", {})
        self.profile.hook_headers = profile.get("hookHeaders", {})

        self.request_order = None
        self.case_id = None
        self.replay_dff_dir = None
        self.case_file = None

    def har2case(self):
        if self.profile.har_file:
            self._convert(os.path.splitext(self.profile.har_file)[0])
        elif self.profile.har_dir and self.profile.des_dir:
            for root, _, files in os.walk(self.profile.har_dir):
                for file in files:
                    if file.endswith(".har"):
                        self.profile.har_file = os.path.join(root, file)
                        self._convert(os.path.splitext(file)[0])
        else:
            logging.error("harFile is null, or, harDir and desDir is null")

    def _convert(self, filename: str):
        if self.profile.des_dir:
            if not os.path.exists(self.profile.des_dir):
                os.makedirs(self.profile.des_dir)
            self.case_file = os.path.join(self.profile.des_dir, "{}_test.py".format(filename))
            self.replay_dff_dir = os.path.join(self.profile.des_dir, "{}-replay-diff".format(filename))
        else:
            self.case_file = "{}_test.py".format(filename)
            self.replay_dff_dir = "{}-replay-diff".format(filename)
        if not self.profile.overwrite and os.path.exists(self.case_file):
            logging.warning('Case file existed, skip "{}"', self.case_file)
            return
        # Generate a unique ID based on the file path
        self.case_id = str(uuid.uuid5(uuid.UUID("3fa83108-6f0a-4cf0-b687-bbdd294ce7fb"), self.case_file)).replace("-", "")
        self.request_order = 1
        logging.info("Start to generate case")
        self._make_case()
        logging.info("Case generated: {}".format(self.case_file))

    def _make_case(self):
        var = self._prepare_var()
        steps = self._prepare_steps()

        content = Har.TEMPLATE.format(var=var, steps=steps)

        if self.profile.replay:
            content = Har.TEMPLATE_IMPORT_REPLAY + content
            if not os.path.exists(self.replay_dff_dir):
                os.makedirs(self.replay_dff_dir)
            content += Har.TEMPLATE_DIFF

        with open(self.case_file, "w") as f:
            f.write(content)

    def _prepare_var(self) -> str:
        var = {}
        if self.profile.hook_var:
            var = self.profile.hook_var
        if self.profile.hook_headers:
            var.update({
                "headers": self.profile.hook_headers
            })
        if self.profile.replay:
            var.update({
                "caseId": self.case_id,
                "requestOrder": 1,
                "diffDir": self.replay_dff_dir
            })
        return str(var)

    def _prepare_steps(self) -> str:
        steps = []
        har_parser = HarParser.from_file(self.profile.har_file)
        for page in har_parser.pages:
            for entry in page.entries:
                step = self._prepare_step(entry)
                steps += step
        return "\n    ".join(steps)

    def _prepare_step(self, entry) -> list:
        logging.info("{} {} Convert step", entry.request.method, entry.request.url)
        step = Step()
        self._make_request_method(step, entry)
        self._make_request_url(step, entry)
        self._make_request_headers(step, entry)
        self._make_request_body(step, entry)
        self._make_before_param(step, entry)
        self._make_after_extract(step, entry)
        self._make_after_assert(step, entry)

        if self.profile.replay:
            self._make_after_replay(step, entry)
            self._save_replay(step, entry)  # Save replay data to sqlite

        return self._make_statement(step, entry)

    def _make_request_method(self, step, entry):
        step.request.method = entry.request.method

    def _make_request_url(self, step, entry):
        step.request.url = entry.request.url

    def _make_request_headers(self, step, entry):
        headers = entry.request.headers
        cookies = entry.request.cookies
        h = dict()
        if self.profile.hook_headers:
            step.request.headers = None  # Move headers to variable pool
        else:
            for header in headers:
                h[header["name"]] = header["value"]
            for cookie in cookies:
                h[cookie["name"]] = cookie["value"]
            if self.profile.json_indent:
                step.request.headers = JSON.beautify_json(json.dumps(h, ensure_ascii=False), self.profile.json_indent)
            else:
                step.request.headers = str(h)

    def _make_request_body(self, step, entry):
        if self.profile.json_indent and entry.request.text:
            step.request.body = JSON.beautify_json(entry.request.text, self.profile.json_indent)
        else:
            step.request.body = entry.request.text

    def _make_before_param(self, step, entry):
        url = step.request.url
        if self.profile.hook_url:
            for k, v in self.profile.hook_url.items():
                url = url.replace(k, v)
        stmt = [
            '',  # Blank line, distinguishing paragraphs
            'url = StringKeyword("{}")'.format(url)
        ]
        if not self.profile.hook_headers:  # If config hookHeaders, move headers to variable pool
            stmt += [
                'headers = JSONKeyword(r"""\n{}\n""")'.format(step.request.headers),
            ]
        body_stmt = [
            'body = JSONKeyword(r"""\n{}\n""")'.format(step.request.body),
        ]
        if step.request.body:
            stmt += body_stmt
        step.before.parametrize = stmt

    def _make_after_extract(self, step, entry):
        stmt = [
            '# user_defined_var = response.jsonpath("$.jsonpath")'
        ]
        step.after.extractor = stmt

    def _make_after_assert(self, step, entry):
        stmt = [
            'assert response.status_code < 400'
        ]
        step.after.assertion = stmt

    def _make_after_replay(self, step, entry):
        stmt = [
            'Sqlite.record_actual((response.text, var["caseId"], var["requestOrder"], "{}", "{}"), var)'.format(step.request.method, step.request.url)
        ]
        step.after.replay = stmt

    def _make_statement(self, step, entry) -> list:
        stmt = []
        stmt += step.before.parametrize
        stmt += [
            'response = HTTPRequestKeyword({})'.format(self._request_param(step, entry))
        ]
        stmt += step.after.extractor
        stmt += step.after.assertion
        stmt += step.after.replay
        return stmt

    def _request_param(self, step, entry) -> str:
        param = ""
        mime_type = entry.request.mimeType
        headers = 'headers'
        if self.profile.hook_headers:
            headers = 'var["headers"]'
        b = 'data=body' if mime_type and mime_type.startswith("application/x-www-form-urlencoded") else 'json=body'
        if step.request.method == "GET":
            if step.request.body:
                param = '"get", url=url, headers={}, params=body'.format(headers)
            else:
                param = '"get", url=url, headers={}'.format(headers)
        if step.request.method == "POST":
            param = '"post", url=url, headers={}, '.format(headers)
            param += b
        if step.request.method == "PUT":
            param = '"put", url=url, headers={}, '.format(headers)
            param += b
        if step.request.method == "DELETE":
            param = '"delete", url=url, headers={}'.format(headers)
        if self.profile.http2:
            param += ', http2=True'
        return param

    def _save_replay(self, step, entry):
        Sqlite.create_table_replay()
        data = (
            self.case_id,
            self.request_order,
            step.request.method,
            step.request.url,
            self._decode_text(entry)
        )
        Sqlite.insert_into_replay_expect(data)
        self.request_order += 1

    def _decode_text(self, entry):
        text = entry.response.text
        if text:
            mime_type = entry.response.mimeType
            if mime_type and mime_type.startswith("application/json"):
                encoding = entry.response.textEncoding
                if encoding and encoding == "base64":
                    content = base64.b64decode(text).decode('utf-8')
                    return content
        return text

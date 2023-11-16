import os

from haralyzer import HarParser
from loguru import logger

from tep.libraries.Step import Step


class Har:
    TEMPLATE = """def test(HTTPRequestKeyword, BodyKeyword):
    var = {var}
    {steps}
"""

    def __init__(self, har_file: str, profile: dict):
        self.har_file = har_file
        self.profile = profile
        filepath = os.path.splitext(self.har_file)[0]
        self.case_file = "{}.py".format(filepath)

    def har2case(self):
        logger.info("Start to generate case")
        self._make_case()
        logger.info("Case generated: {}".format(self.case_file))

    def _make_case(self):
        var = self._prepare_var()
        steps = self._prepare_steps()

        content = Har.TEMPLATE.format(var=var, steps=steps)
        with open(self.case_file, "w") as f:
            f.write(content)

    def _prepare_var(self) -> str:
        var = {}
        return str(var)

    def _prepare_steps(self) -> str:
        steps = []
        har_parser = HarParser.from_file(self.har_file)
        for page in har_parser.pages:
            for entry in page.entries:
                step = self._prepare_step(entry)
                steps += step
        return "\n    ".join(steps)

    def _prepare_step(self, entry) -> list:
        logger.info("{} {} Convert step", entry.request.method, entry.request.url)
        step = Step()
        self._make_request_method(step, entry)
        self._make_request_url(step, entry)
        self._make_request_headers(step, entry)
        self._make_request_body(step, entry)
        self._make_before_param(step, entry)
        self._make_after_extract(step, entry)
        self._make_after_assert(step, entry)
        return self._make_statement(step)

    def _make_request_method(self, step, entry):
        step.request.method = entry.request.method

    def _make_request_url(self, step, entry):
        step.request.url = entry.request.url

    def _make_request_headers(self, step, entry):
        headers = entry.request.headers
        cookies = entry.request.cookies
        h = dict()
        for header in headers:
            h[header["name"]] = header["value"]
        for cookie in cookies:
            h[cookie["name"]] = cookie["value"]
        step.request.headers = h

    def _make_request_body(self, step, entry):
        step.request.body = entry.request.text

    def _make_before_param(self, step, entry):
        stmt = [
            '',  # Blank line, distinguishing paragraphs
            'url = "{}"'.format(step.request.url),
            'headers = {}'.format(step.request.headers),
        ]
        body_stmt = [
            'body = r"""{}"""'.format(step.request.body),
            'ro = BodyKeyword(body)',
            '# ro = BodyKeyword(body, {"$.jsonpath": "value"})',
            'body = ro.data'
        ]
        if step.request.body:
            stmt += body_stmt
        step.before.parametrize = stmt

    def _make_after_extract(self, step, entry):
        stmt = [
            '# user_defined_var = ro.response.jsonpath("$.jsonpath")'
        ]
        step.after.extractor = stmt

    def _make_after_assert(self, step, entry):
        stmt = [
            'assert ro.response.status_code < 400'
        ]
        step.after.assertion = stmt

    def _make_statement(self, step) -> list:
        stmt = []
        stmt += step.before.parametrize
        stmt += [
            'ro = HTTPRequestKeyword({})'.format(self._request_param(step))
        ]
        stmt += step.after.extractor
        stmt += step.after.assertion
        return stmt

    def _request_param(self, step) -> str:
        param = ""
        if step.request.method == "GET":
            param = '"get", url=url, headers=headers, params=body' if step.request.body else '"get", url=url, headers=headers'
        if step.request.method == "POST":
            param = '"post", url=url, headers=headers, json=body'
        if step.request.method == "PUT":
            param = '"put", url=url, headers=headers, json=body'
        if step.request.method == "DELETE":
            param = '"delete", url=url, headers=headers'
        if self.profile.get("http2", False):
            param += ', http2=True'
        return param

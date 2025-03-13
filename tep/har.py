#!/usr/bin/python
# encoding=utf-8
import logging
import os

from haralyzer import HarParser

from tep.patch import patch_json


def har2case(settings: dict):
    Har(settings).har2case()


class Settings:
    def __init__(self):
        self.har_path: str = ''
        self.des_dir: str = ''
        self.overwrite: bool = False
        self.json_indent: int = 4
        self.http2: bool = False
        self.hook_variable: dict = {}
        self.hook_url: dict = {}
        self.hook_headers: dict = {}


class Har:
    TEMPLATE = '''from tep import request
from tep import v


class Data:
    v({variable})
{data}

def test():
{case}
'''

    def __init__(self, settings: dict):
        self.settings = Settings()
        self.settings.har_path = settings.get('har', '')
        self.settings.des_dir = settings.get('dir', '')
        self.settings.overwrite = settings.get('overwrite', False)
        self.settings.http2 = settings.get('http2', False)
        self.settings.hook_variable = settings.get('var', {})
        self.settings.hook_url = settings.get('url', {})
        self.settings.hook_headers = settings.get('headers', {})

        self.har_file = None
        self.case_file = None
        self.data = []
        self.body_id = 1

    def har2case(self):
        if not self.settings.har_path:
            logging.error('Har path is None')
            return

        if os.path.isfile(self.settings.har_path):
            self.har_file = self.settings.har_path
            self._convert()
        else:
            for root, _, files in os.walk(self.settings.har_path):
                for file in files:
                    if file.endswith('.har'):
                        self.har_file = os.path.join(root, file)
                        self._convert()

    def _convert(self):
        filename = os.path.splitext(os.path.basename(self.har_file))[0]
        if not os.path.exists(self.settings.des_dir):
            os.makedirs(self.settings.des_dir)
        self.case_file = os.path.join(self.settings.des_dir, 'test_{}.py'.format(filename))
        if not self.settings.overwrite and os.path.exists(self.case_file):
            logging.warning('Case file existed, skip: {}', self.case_file)
            return
        logging.info('Start to generate case')
        self._make_case()
        logging.info('Case generated: {}'.format(self.case_file))

    def _make_case(self):
        self._generate_variable()
        case = self._generate_case()
        variable = patch_json.dumps(self.variable)
        data = ''.join(self.data)
        content = Har.TEMPLATE.format(variable=variable, case=case, data=data)
        with open(self.case_file, 'w') as f:
            f.write(content)

    def _generate_variable(self):
        variable = {'domain': ''}
        if self.settings.hook_variable:
            variable.update(self.settings.hook_variable)
        if self.settings.hook_headers:
            self.data.append(f'    headers = {self.settings.hook_headers}\n')
        self.variable = variable

    def _generate_case(self) -> str:
        steps = []
        har_parser = HarParser.from_file(self.har_file)
        for page in har_parser.pages:
            for entry in page.entries:
                step = self._generate_step(entry)
                steps += step
        return '\n    '.join(steps)

    def _generate_step(self, entry) -> list:
        logging.info(f'{entry.request.method} {entry.request.url} Convert step')
        step = Step()
        self._make_request_method(step, entry)
        self._make_request_url(step, entry)
        self._make_request_headers(step, entry)
        self._make_request_body(step, entry)
        self._make_before_param(step, entry)
        self._make_after_extract(step, entry)
        self._make_after_assert(step, entry)
        return self._make_statement(step, entry)

    def _make_request_method(self, step, entry):
        step.request.method = entry.request.method

    def _make_request_url(self, step, entry):
        step.request.url = entry.request.url

    def _make_request_headers(self, step, entry):
        headers = entry.request.headers
        cookies = entry.request.cookies
        h = dict()
        if self.settings.hook_headers:
            step.request.headers = None  # Move headers to variable
        else:
            for header in headers:
                h[header['name']] = header['value']
            for cookie in cookies:
                h[cookie['name']] = cookie['value']
            step.request.headers = patch_json.simplify(patch_json.dumps(h))

    def _make_request_body(self, step, entry):
        if entry.request.text:
            step.request.body = patch_json.simplify(entry.request.text)
        else:
            step.request.body = entry.request.text

    def _make_before_param(self, step, entry):
        url = step.request.url
        if self.settings.hook_url:
            for k, v in self.settings.hook_url.items():
                url = url.replace(k, v)
        stmt = [
            '',  # Blank line, distinguishing paragraphs
            "url = v('{}')".format(url)
        ]
        if not self.settings.hook_headers:  # If config hookHeaders, move headers to variable
            stmt += [
                "headers = v(r'''{}''')".format(step.request.headers),
            ]
        body_stmt = [
            f'body = v(Data.body_{self.body_id})',
        ]
        if step.request.body:
            stmt += body_stmt
            self.data.append(f"    body_{self.body_id} = '{step.request.body}'\n")
            self.body_id += 1
        step.before.parametrize = stmt

    def _make_after_extract(self, step, entry):
        stmt = [
            "# v('name', response.jsonpath('$.jsonpath')[0])"
        ]
        step.after.extractor = stmt

    def _make_after_assert(self, step, entry):
        stmt = [
            'assert response.status_code < 400'
        ]
        step.after.assertion = stmt

    def _request_param(self, step, entry) -> str:
        param = ''
        mime_type = entry.request.mimeType
        headers = 'headers'
        if self.settings.hook_headers:
            headers = 'Data.headers'
        b = 'data=body' if mime_type and mime_type.startswith('application/x-www-form-urlencoded') else 'json=body'
        if step.request.method == 'GET':
            if step.request.body:
                param = "'get', url=url, headers={}, params=body".format(headers)
            else:
                param = "'get', url=url, headers={}".format(headers)
        if step.request.method == 'POST':
            param = "'post', url=url, headers={}, ".format(headers)
            param += b
        if step.request.method == 'PUT':
            param = "'put', url=url, headers={}, ".format(headers)
            param += b
        if step.request.method == 'DELETE':
            param = "'delete', url=url, headers={}".format(headers)
        if self.settings.http2:
            param += ', http2=True'
        return param

    def _make_statement(self, step, entry) -> list:
        stmt = []
        stmt += step.before.parametrize
        stmt += [
            'response = request({})'.format(self._request_param(step, entry))
        ]
        stmt += step.after.extractor
        stmt += step.after.assertion
        return stmt


class Request:
    method: str = ''
    url: str = ''
    headers: str = ''
    body: str = ''


class Before:
    def __init__(self):
        self.parametrize: list = []


class After:
    def __init__(self):
        self.extractor: list = []
        self.assertion: list = []


class Step:
    def __init__(self):
        self.name: str = ''
        self.before: Before = Before()
        self.request: Request = Request()
        self.after: After = After()

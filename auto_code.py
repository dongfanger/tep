#!/usr/bin/python
# encoding=utf-8

"""
@Author :  dongfanger
@Date   :  2020/2/12 22:15
@Desc   :  auto generate api and test code
"""

import os
import re

from common.func import current_time


class AutoCode:
    def __init__(self, author, api_info):
        self.author = author
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.description = api_info['api_description']
        self.api_dir = os.path.join(os.path.join(self.base_dir, 'api'), api_info['api_dir'])
        self.uri = api_info['uri']
        self.body = api_info['body']
        self.case_dir = os.path.join(os.path.join(self.base_dir, 'case'), api_info['case_dir'])

        if not os.path.exists(self.api_dir):
            os.system(f'mkdir {self.api_dir}')
        if not os.path.exists(self.case_dir):
            os.system(f'mkdir {self.case_dir}')

        if not self.uri.startswith('/'):
            self.uri = '/' + self.uri

        self.module_name = self.uri2filename(self.uri)
        self.classname = self.uri2classname(self.uri)

        self.api_file_path = os.path.join(self.api_dir, self.classname + '.py')
        self.case_file_path = os.path.join(self.case_dir, 'test' + self.module_name + '.py')

    @staticmethod
    def uri2filename(u):
        """underline style"""
        return u.replace('/', '_')

    @staticmethod
    def uri2classname(u):
        """camel style"""
        u = u[1].upper() + u[2:]
        chars = re.findall('/.|_.', u)
        for c in chars:
            u = u.replace(c, c[1].upper())
        return u

    @staticmethod
    def jmeter_transfer(j):
        j = j.replace("null", '""').replace("false", "False").replace('true', 'True')
        s = re.findall('"?\\${.*?}"?', j)
        for x in s:
            if x.startswith('"'):
                j = j.replace(x, 'f"' + '{self.' + x[3:])
            else:
                j = j.replace(x, 'self.' + x[2:-1])
        return j

    def generate_code(self):
        api_code_template = f"""#!/usr/bin/python
# encoding=utf-8

\"\"\"
@Author :  {self.author}
@Date   :  {current_time()}
@Desc   :  {self.description}
\"\"\"

from api.base import Api
from pytest_allure import vars_


class {self.classname}(Api):

    def __init__(self):
        super().__init__()
        self.url = vars_.test_url + "{self.uri}"

    def load(self):
        self.body = {self.jmeter_transfer(self.body)}
        return self

    def send(self):
        self.res = self.req.post(url=self.url, headers=vars_.headers, json=self.body)
        self.assert_response_status()
        return self.res
"""
        api_import_name = (self.api_dir.replace(self.base_dir, '')[1:].replace('/', '.').replace('\\', '.')
                           + '.' + self.classname)
        case_code_template = f"""#!/usr/bin/python
# encoding=utf-8

\"\"\"
@Author :  {self.author}
@Date   :  {current_time()}
@Desc   : 
\"\"\"

from {api_import_name} import {self.classname}
from pytest_allure import vars_


def test_default():
    x = {self.classname + '()'}
    x.load().send()
"""
        return api_code_template, case_code_template


def test():
    author = 'dongfanger'
    api_info = {
        'api_description': 'demo',
        'api_dir': 'bu',
        'uri': '/mock/hello/pyface',
        'body': """{}""",
        'case_dir': 'demo',
    }
    ag = AutoCode(author, api_info)
    api_code, case_code = ag.generate_code()

    if os.path.exists(ag.api_file_path):
        print(f'\napi create failed, api existed, the path is {ag.api_file_path}')
    else:
        with open(ag.api_file_path, 'w') as f:
            f.writelines(api_code)
            print(f'api create success, the path is {ag.api_file_path}')

    if os.path.exists(ag.case_file_path):
        print(f'case create failed, case existed, the path is {ag.case_file_path}')
    else:
        with open(ag.case_file_path, 'w') as f:
            f.writelines(case_code)
            print(f'case create success, the path is {ag.case_file_path}')

#!/usr/bin/python
# encoding=utf-8

"""
@Author : Dongfanger
@Date   :  2020/2/12 22:15
@Desc   :  Auto generate api and test code
"""

import os
import re

from common.func import current_time


class AutoCode:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.api_dir = os.path.join(os.path.join(self.base_dir, 'api'), 'bu')  # 1
        self.case_dir = os.path.join(os.path.join(self.base_dir, 'case'), 'sprint')  # 2
        self.uri = '/api/post'  # 3
        self.description = 'Demo auto code'  # 4
        # 5
        self.body = """{}
"""
        self.name = self.uri2name(self.uri)
        if not os.path.exists(self.api_dir):
            os.system(f'mkdir {self.api_dir}')
        if not os.path.exists(self.case_dir):
            os.system(f'mkdir {self.case_dir}')
        self.api_file_path = os.path.join(self.api_dir, self.name + '.py')
        self.case_file_path = os.path.join(self.case_dir, 'test_' + self.name + '.py')

    @staticmethod
    def uri2name(u):
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
@Author : Dongfanger
@Date   :  {current_time()}
@Desc   :  {self.description}
\"\"\"

from api.base import Api
from data.env import vars_


class {self.name}(Api):

    def __init__(self):
        super().__init__()
        self.url = vars_.test_url + "{self.uri}"

    def load(self):
        self.body = {self.jmeter_transfer(self.body)}
        return self

    def send(self):
        self.res = self.req.post(url=self.url, headers=vars_.headers, json=self.body)
        self.set_content()
        return self.res
"""
        api_import_name = (self.api_dir.replace(self.base_dir, '')[1:].replace('/', '.').replace('\\', '.')
                           + '.' + self.name)
        case_code_template = f"""#!/usr/bin/python
# encoding=utf-8

\"\"\"
@Author : Dongfanger
@Date   :  {current_time()}
@Desc   : 
\"\"\"

from {api_import_name} import {self.name}
from data.env import vars_


def test_default():
    x = {self.name + '()'}
    x.load().send()
"""
        return api_code_template, case_code_template


def test():
    ag = AutoCode()
    api_code, case_code = ag.generate_code()

    if os.path.exists(ag.api_file_path):
        print(f'Api create failed, api existed, the path is {ag.api_file_path}')
    else:
        with open(ag.api_file_path, 'w') as f:
            f.writelines(api_code)
            print(f'Api create success, the path is {ag.api_file_path}')

    if os.path.exists(ag.case_file_path):
        print(f'Case create failed, case existed, the path is {ag.case_file_path}')
    else:
        with open(ag.case_file_path, 'w') as f:
            f.writelines(case_code)
            print(f'Case create success, the path is {ag.case_file_path}')

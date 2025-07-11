#!/usr/bin/python
# encoding=utf-8

import os
import platform
import sys

from tep.config import Config
from tep.patch.patch_logging import logger


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser('new', help='Create a new project with template structure.')
    sub_parser_scaffold.add_argument('project_name', type=str, nargs='?', help='Specify new project name.')
    sub_parser_scaffold.add_argument(
        '-venv',
        dest='create_venv',
        action='store_true',
        help='Create virtual environment in the project, and install tep.',
    )
    return sub_parser_scaffold


def scaffold(args):
    Config.CREATE_VENV = args.create_venv
    sys.exit(create_scaffold(args.project_name))


def create_scaffold(project_name):
    if os.path.isdir(project_name):
        logger.warning(f'Project folder {project_name} exists, please specify a new project name')
        return 1
    elif os.path.isfile(project_name):
        logger.warning(f'Project name {project_name} conflicts with existed file, please specify a new one')
        return 1

    print(f'Create new project: {project_name}')
    print(f'Project root dir: {os.path.join(os.getcwd(), project_name)}\n')

    def create_folder(path):
        os.makedirs(path)
        msg = f'Created folder: {path}'
        print(msg)

    def create_file(path, file_content=''):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        msg = f'Created file:   {path}'
        print(msg)

    create_folder(project_name)
    create_folder(os.path.join(project_name, 'data'))
    create_folder(os.path.join(project_name, 'file'))
    create_folder(os.path.join(project_name, 'file', 'har'))
    create_folder(os.path.join(project_name, 'fixture'))
    create_folder(os.path.join(project_name, 'function'))
    create_folder(os.path.join(project_name, 'report'))
    create_folder(os.path.join(project_name, 'scripts'))
    create_folder(os.path.join(project_name, 'tests'))

    create_file(os.path.join(project_name, '.gitignore'), '''.idea
.pytest_cache/
__pycache__/
.venv
.har
    ''')

    create_file(os.path.join(project_name, 'conftest.py'), '''from tep.plugin import tep_plugins

pytest_plugins = tep_plugins()
''')

    create_file(os.path.join(project_name, 'pytest.ini'), '''[pytest]
log_cli = True
log_level = INFO
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
''')

    create_file(os.path.join(project_name, 'run.py'), '''from tep import run

if __name__ == '__main__':
    run({
        'path': ['test_flow.py'],  # Relative path to tests, file or directory
        'report': 1  # Generate html report, 0: False, 1: True
    })
''')

    create_file(os.path.join(project_name, 'data', '__init__.py'), '')

    create_file(os.path.join(project_name, 'data', 'GlobalData.py'), '''#!/usr/bin/python
# encoding=utf-8


class GlobalData:
    domain = 'http://127.0.0.1:5000'
    headers = {'Content-Type': 'application/json', 'Cookie': 'de2e3ffu29'}
''')

    create_file(os.path.join(project_name, 'fixture', '__init__.py'), '')

    create_file(os.path.join(project_name, 'fixture', 'fixture_login.py'), '''#!/usr/bin/python
# encoding=utf-8

import pytest
from tep import request


@pytest.fixture(scope='session')
def login():
    url = 'http://127.0.0.1:5000/login'
    headers = {'Content-Type': 'application/json'}
    body = {'username': 'dongfanger', 'password': '123456'}
    response = request('post', url=url, headers=headers, json=body)
    assert response.status_code < 400
    return {'Content-Type': 'application/json', 'Cookie': f'{response.json()["Cookie"]}'}
''')

    create_file(os.path.join(project_name, 'function', '__init__.py'), '')

    create_file(os.path.join(project_name, 'function', 'common.py'), '''#!/usr/bin/python
# encoding=utf-8
import os.path

from tep import file


def base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def headers():
    return {'Content-Type': 'application/json', 'Cookie': file(os.path.join(base_dir(), 'file', 'Cookie'))}
''')

    create_file(os.path.join(project_name, 'scripts', 'mock.py'), '''import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.post('/login')
async def login(req: Request):
    body = await req.json()
    if body['username'] == 'dongfanger' and body['password'] == '123456':
        return {'Cookie': 'de2e3ffu29'}
    return ''


@app.get('/searchSku')
async def search_sku(req: Request):
    if req.headers.get('Cookie') == 'de2e3ffu29' and req.query_params.get('skuName') == 'book':
        return {'skuId': '222', 'price': '2.3'}
    return ''


@app.post('/addCart')
async def add_cart(req: Request):
    body = await req.json()
    if req.headers.get('Cookie') == 'de2e3ffu29' and body['skuId'] == '222':
        return {'skuId': '222', 'price': '2.3', 'skuNum': 3, 'totalPrice': '6.9'}
    return ''


@app.post('/order')
async def order(req: Request):
    body = await req.json()
    if req.headers.get('Cookie') == 'de2e3ffu29' and body['skuId'] == '222':
        return {'orderId': '333'}
    return ''


@app.post('/pay')
async def pay(req: Request):
    body = await req.json()
    if req.headers.get('Cookie') == 'de2e3ffu29' and body['orderId'] == '333':
        return {'success': 'true'}
    return ''


@app.get('/retry/code', status_code=500)
async def retry_code(req: Request):
    return {'success': 'false'}


if __name__ == '__main__':
    uvicorn.run('mock:app', host='127.0.0.1', port=5000)
''')

    create_file(os.path.join(project_name, 'tests', 'test_get.py'), '''from tep import request


def test():
    response = request('get', url='http://httpbin.org/status/200')
    assert response.status_code == 200
''')

    create_file(os.path.join(project_name, 'tests', 'test_flow.py'), '''from tep import request
from tep import v

from data.GlobalData import GlobalData


class Data:
    v({
        'domain': GlobalData.domain,
        'skuNum': 2,
        'payAmount': 0.2
    })
    body_add_cart = '{'skuId':'${skuId}','skuNum':${skuNum}}'
    body_order = '{'skuId':'${skuId}','price':${skuPrice},'skuNum':${skuNum},'totalPrice':${totalPrice}}'
    body_pay = '{'orderId':'${orderId}','payAmount':${payAmount}}'


def test():
    url = v('${domain}/searchSku?skuName=book')
    response = request('get', url=url, headers=GlobalData.headers)
    assert response.status_code < 400
    v('skuId', response.jsonpath('$.skuId')[0])
    v('skuPrice', response.jsonpath('$.price')[0])

    url = v('${domain}/addCart')
    body = v(Data.body_add_cart)
    response = request('post', url=url, headers=GlobalData.headers, json=body)
    assert response.status_code < 400
    v('skuNum', response.jsonpath('$.skuNum')[0])
    v('totalPrice', response.jsonpath('$.totalPrice')[0])

    url = v('${domain}/order')
    body = v(Data.body_order)
    response = request('post', url=url, headers=GlobalData.headers, json=body)
    assert response.status_code < 400
    v('orderId', response.jsonpath('$.orderId')[0])

    url = v('${domain}/pay')
    body = v(Data.body_pay)
    response = request('post', url=url, headers=GlobalData.headers, json=body)
    assert response.status_code < 400
    assert response.jsonpath('$.success')[0] == 'true'
''')

    if Config.CREATE_VENV:
        # Create Python virtual Environment
        os.chdir(project_name)
        print('\nCreating virtual environment')
        os.system('python -m venv .venv')
        print('Created virtual environment: .venv')

        # Install tep in the Python virtual Environment
        print('Installing tep')
        if platform.system().lower() == 'windows':
            os.chdir('.venv')
            os.chdir('Scripts')
            os.system('pip install tep')
        elif platform.system().lower() == 'linux':
            os.chdir('.venv')
            os.chdir('bin')
            os.system('pip install tep')

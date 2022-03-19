#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2021/11/13 17:50
@Desc    :  
"""

gitignore_content = """.idea/
.pytest_cache/
.tep_allure_tmp/
__pycache__/
*.pyc
reports/
debug/"""

conf_yaml_content = """env: qa"""

conftest_content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" 只能管理员编辑，只对外提供fixture。
\"\"\"

import os
import time

import pytest

# 项目目录路径
_project_dir = os.path.dirname(os.path.abspath(__file__))


# 设置缓存供tep使用
@pytest.fixture(scope="session", autouse=True)
def _project_cache(request):
    request.config.cache.set("project_dir", _project_dir)


# 自动导入fixtures
_fixtures_dir = os.path.join(_project_dir, "fixtures")
_fixtures_paths = []
for root, _, files in os.walk(_fixtures_dir):
    for file in files:
        if file.startswith("fixture_") and file.endswith(".py"):
            full_path = os.path.join(root, file)
            import_path = full_path.replace(_fixtures_dir, "").replace("\\\\", ".").replace("/", ".").replace(".py", "")
            _fixtures_paths.append("fixtures" + import_path)
pytest_plugins = _fixtures_paths


# pytest hook函数
# https://docs.pytest.org/en/latest/reference/reference.html#hooks
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    duration = time.time() - terminalreporter._sessionstarttime
"""

pytest_ini_content = """[pytest]
markers =
    smoke: 冒烟测试
    regress: 回归测试
"""

fixture_env_vars_content = """#!/usr/bin/python
# encoding=utf-8

from tep.dao import mysql_engine
from tep.fixture import *


@pytest.fixture(scope="session")
def env_vars(config):
    class Clazz(TepVars):
        env = config["env"]

        \"\"\"变量定义开始\"\"\"
        # 环境变量
        mapping = {
            "qa": {  # qa环境
                "domain": "http://127.0.0.1:5000",  # 变量名:变量值
                "mysql_engine": mysql_engine("127.0.0.1",  # host
                                             "2306",  # port
                                             "root",  # username
                                             "123456",  # password
                                             "qa"),  # dbname
            },
            "release": {  # release环境
                "domain": "https://release.com",  # 变量名:变量值
                "mysql_engine": mysql_engine("127.0.0.1",
                                             "2306",
                                             "root",
                                             "123456",
                                             "release"),
            }
            # 继续添加
        }
        # 定义类属性，敲代码时会自动补全
        domain = mapping[env]["domain"]
        mysql_engine = mapping[env]["mysql_engine"]
        \"\"\"变量定义结束\"\"\"

    return Clazz()
"""

fixture_login_content = """from tep.client import request
from tep.fixture import *


def _jwt_headers(token):
    return {"Content-Type": "application/json", "authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def login(env_vars):
    # 封装登录接口
    logger.info("Administrator login")
    response = request(
        "post",
        url=env_vars.domain + "/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": "dongfanger",
            "password": "123456",
        }
    )
    assert response.status_code < 400
    response_token = jmespath.search("token", response.json())

    class Clazz:
        token = response_token
        jwt_headers = _jwt_headers(response_token)

    return Clazz
"""

test_login_content = """from loguru import logger


def test_login(login):
    logger.info(login.token)
"""

test_mysql_content = """from loguru import logger
from tep.dao import print_db_table


def test_mysql(pd, env_vars):
    data = pd.read_sql("select 1 from dual", env_vars.mysql_engine)
    logger.info(print_db_table(data))
"""

test_request_content = """from urllib.parse import urlencode

from tep.client import request

# -------------------------------get开始-------------------------------
# 不带参数
request("get", url="/api/xxx", headers={})
# json参数
request("get", url="/api/xxx", headers={}, params={})
# queryset
request("get", url="/api/xxx?a=1&b=2", headers={})
# json转queryset
query = {}
request("get", url="/api/xxx" + "?" + urlencode(query), headers={})
# -------------------------------get结束-------------------------------

# -------------------------------post开始-------------------------------
# json参数
request("post", url="/api/xxx", headers={}, json={})

# dict参数
request("post", url="/api/xxx", headers={}, data={})
# -------------------------------post结束-------------------------------

# -------------------------------put开始-------------------------------
request("put", url="/api/xxx", headers={}, json={})
# -------------------------------post结束-------------------------------

# -------------------------------delete开始-------------------------------
request("delete", url=f"/api/xxx", headers={})
# -------------------------------delete结束-------------------------------

# -------------------------------上传excel开始-------------------------------
file_name = ""
file_path = ""
request("post",
        url="",
        headers={},
        files={
            "file": (
                file_name,
                open(file_path, "rb"),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        },
        verify=False
        )
# -------------------------------上传excel结束-------------------------------
"""

fastapi_mock_content = """#!/usr/bin/python
# encoding=utf-8

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/login")
async def login(req: Request):
    body = await req.json()
    if body["username"] == "dongfanger" and body["password"] == "123456":
        return {"token": "de2e3ffu29"}
    return ""


@app.get("/searchSku")
def search_sku(req: Request):
    if req.headers.get("token") == "de2e3ffu29" and req.query_params.get("skuName") == "电子书":
        return {"skuId": "222", "price": "2.3"}
    return ""


@app.post("/addCart")
async def add_cart(req: Request):
    body = await req.json()
    if req.headers.get("token") == "de2e3ffu29" and body["skuId"] == "222":
        return {"skuId": "222", "price": "2.3", "skuNum": "3", "totalPrice": "6.9"}
    return ""


@app.post("/order")
async def order(req: Request):
    body = await req.json()
    if req.headers.get("token") == "de2e3ffu29" and body["skuId"] == "222":
        return {"orderId": "333"}
    return ""


@app.post("/pay")
async def pay(req: Request):
    body = await req.json()
    if req.headers.get("token") == "de2e3ffu29" and body["orderId"] == "333":
        return {"success": "true"}
    return ""


if __name__ == '__main__':
    uvicorn.run("fastapi_mock:app", host="127.0.0.1", port=5000)
"""

http_client_content = """#!/usr/bin/python
# encoding=utf-8

import decimal
import json
import time

import allure
from loguru import logger
from tep import client


def request_monkey_patch(req, *args, **kwargs):
    start = time.process_time()
    desc = ""
    if "desc" in kwargs:
        desc = kwargs.get("desc")
        kwargs.pop("desc")
    response = req(*args, **kwargs)
    end = time.process_time()
    elapsed = str(decimal.Decimal("%.3f" % float(end - start))) + "s"
    log4a = "{}\\n{}status:{}\\nresponse:{}\\nelapsed:{}"
    try:
        kv = ""
        for k, v in kwargs.items():
            # if not json, str()
            try:
                v = json.dumps(v, ensure_ascii=False)
            except TypeError:
                v = str(v)
            kv += f"{k}:{v}\\n"
        args = list(args)
        args += ["", ""]
        method, url, *t = args
        method_url = ""
        if method:
            method_url = f'\\nmethod:"{method}" '
        if url:
            method_url += f'\\nurl:"{url}" '
        request_response = log4a.format(method_url, kv, response.status_code, response.text, elapsed)
        logger.info(request_response)
        allure.attach(request_response, f'{desc} request & response', allure.attachment_type.TEXT)
    except AttributeError:
        logger.error("request failed")
    except TypeError:
        logger.warning(log4a)
    return response


def request(method, url, **kwargs):
    client.tep_request_monkey_patch = request_monkey_patch
    return client.request(method, url, **kwargs)
"""

test_login_pay_content = """import jmespath
from tep.client import request

\"\"\"
测试登录到下单流程，需要先运行utils/fastapi_mock.py
\"\"\"


def test(env_vars, login):
    # 搜索商品
    response = request(
        "get",
        url=env_vars.domain + "/searchSku",
        headers={"token": login.token},
        params={"skuName": "电子书"}
    )
    sku_id = jmespath.search("skuId", response.json())
    sku_price = jmespath.search("price", response.json())
    assert response.status_code < 400

    # 添加购物车
    sku_num = 3
    response = request(
        "post",
        url=env_vars.domain + "/addCart",
        headers={"token": login.token},
        json={"skuId": sku_id, "skuNum": str(sku_num)}
    )
    total_price = jmespath.search("totalPrice", response.json())
    assert response.status_code < 400

    # 下单
    response = request(
        "post",
        url=env_vars.domain + "/order",
        headers={"token": login.token},
        json={"skuId": sku_id, "price": sku_price, "skuNum": str(sku_num), "totalPrice": total_price}
    )
    order_id = jmespath.search("orderId", response.json())
    assert response.status_code < 400

    # 支付
    response = request(
        "post",
        url=env_vars.domain + "/pay",
        headers={"token": login.token},
        json={"orderId": order_id, "payAmount": "6.9"}
    )
    assert response.status_code < 400
    assert response.json()["success"] == "true"
"""

Login_content = """from tep.client import BaseRequest


class Login(BaseRequest):

    def post(self):
        response = self.request(
            "post",
            url=self.case_vars.get("domain") + "/login",
            headers={"Content-Type": "application/json"},
            json={
                "username": "dongfanger",
                "password": "123456",
            }
        )
        assert response.status_code < 400
        self.case_vars.put("token", response.jmespath("token"))
"""

SearchSku_content = """from tep.client import BaseRequest


class SearchSku(BaseRequest):

    def get(self):
        response = self.request(
            "get",
            url=self.case_vars.get("domain") + "/searchSku",
            headers={"token": self.case_vars.get("token")},
            params={"skuName": "电子书"}
        )
        self.case_vars.put("skuId", response.jmespath("skuId"))
        self.case_vars.put("skuPrice", response.jmespath("price"))
        assert response.status_code < 400
"""

AddCart_content = """from tep.client import BaseRequest


class AddCart(BaseRequest):

    def post(self):
        response = self.request(
            "post",
            url=self.case_vars.get("domain") + "/addCart",
            headers={"token": self.case_vars.get("token")},
            json={"skuId": self.case_vars.get("skuId"), "skuNum": self.case_vars.get("skuNum")}
        )
        self.case_vars.put("totalPrice", response.jmespath("totalPrice"))
        assert response.status_code < 400
"""

Order_content = """from tep.client import BaseRequest


class Order(BaseRequest):

    def post(self):
        response = self.request(
            "post",
            url=self.case_vars.get("domain") + "/order",
            headers={"token": self.case_vars.get("token")},
            json={"skuId": self.case_vars.get("skuId"), "price": self.case_vars.get("skuPrice"),
                  "skuNum": self.case_vars.get("skuNum"), "totalPrice": self.case_vars.get("totalPrice")}
        )
        self.case_vars.put("orderId", response.jmespath("orderId"))
        assert response.status_code < 400
"""

Pay_content = """from tep.client import BaseRequest


class Pay(BaseRequest):

    def post(self):
        response = self.request(
            "post",
            url=self.case_vars.get("domain") + "/pay",
            headers={"token": self.case_vars.get("token")},
            json={"orderId": self.case_vars.get("orderId"), "payAmount": "6.9"}
        )
        assert response.status_code < 400
        assert response.jmespath("success") == "true"
"""

test_login_pay_mvc_content = """from tep.fixture import TepVars

from samples.login_pay.mvc.services.AddCart import AddCart
from samples.login_pay.mvc.services.Login import Login
from samples.login_pay.mvc.services.Order import Order
from samples.login_pay.mvc.services.Pay import Pay
from samples.login_pay.mvc.services.SearchSku import SearchSku

\"\"\"
测试登录到下单流程，需要先运行utils / fastapi_mock.py
\"\"\"


class Test:
    case_vars = TepVars()
    case_vars.vars_ = {
        "domain": "http://127.0.0.1:5000",
        "skuNum": "3"
    }

    def test(self):
        # 登录
        Login(Test).post()
        # 搜索商品
        SearchSku(Test).get()
        # 添加购物车
        AddCart(Test).post()
        # 下单
        Order(Test).post()
        # 支付
        Pay(Test).post()
"""

test_request_monkey_patch_content = """from utils.http_client import request


def test_login(env_vars):
    response = request(
        "post",
        url=env_vars.domain + "/login",
        desc="登录",
        headers={"Content-Type": "application/json"},
        json={
            "username": "dongfanger",
            "password": "123456",
        }
    )
    assert response.status_code < 400
"""

mitm_content = """#!/usr/bin/python
# encoding=utf-8

# mitmproxy录制流量自动生成用例

import os
import time

from mitmproxy import ctx

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tests_dir = os.path.join(project_dir, "tests")
# tests/mitm
mitm_dir = os.path.join(tests_dir, "mitm")
if not os.path.exists(mitm_dir):
    os.mkdir(mitm_dir)
# 当前时间作为文件名
filename = f'test_{time.strftime("%Y%m%d_%H%M%S", time.localtime())}.py'
case_file = os.path.join(mitm_dir, filename)
# 生成用例文件
template = \"\"\"import allure
from tep.client import request


@allure.title("")
def test(env_vars):
\"\"\"
if not os.path.exists(case_file):
    with open(case_file, "w", encoding="utf8") as fw:
        fw.write(template)


class Record:
    def __init__(self, domains):
        self.domains = domains

    def response(self, flow):
        if self.match(flow.request.url):
            # method
            method = flow.request.method.lower()
            ctx.log.error(method)
            # url
            url = flow.request.url
            ctx.log.error(url)
            # headers
            headers = dict(flow.request.headers)
            ctx.log.error(headers)
            # body
            body = flow.request.text or {}
            ctx.log.error(body)
            with open(case_file, "a", encoding="utf8") as fa:
                fa.write(self.step(method, url, headers, body))

    def match(self, url):
        if not self.domains:
            ctx.log.error("必须配置过滤域名")
            exit(-1)
        for domain in self.domains:
            if domain in url:
                return True
        return False

    def step(self, method, url, headers, body):
        if method == "get":
            body_grammar = f"params={body}"
        else:
            body_grammar = f"json={body}"
        return f\"\"\"
    # 描述
    # 数据
    # 请求
    response = request(
        "{method}",
        url="{url}",
        headers={headers},
        {body_grammar}
    )
    # 提取
    # 断言
    assert response.status_code < 400
\"\"\"


# ==================================配置开始==================================
addons = [
    Record(
        # 过滤域名
        [
            "http://www.httpbin.org",
            "http://127.0.0.1:5000"
        ],
    )
]
# ==================================配置结束==================================

\"\"\"
==================================命令说明开始==================================
# 正向代理（需要手动打开代理）
mitmdump -s mitm.py
# 反向代理
mitmdump -s mitm.py --mode reverse:http://127.0.0.1:5000 --listen-host 127.0.0.1 --listen-port 8000
==================================命令说明结束==================================
\"\"\"
"""

structure_content = """项目结构说明：
files：文件
fixtures：pytest fixture
reports：allure测试报告
samples：示例代码
  db：数据库
    test_mysql.py：连接MySQL
  http：requests请求
    test_request.py：requests常见用法
    test_request_monkey_patch.py：tep request猴子补丁测试
  login_pay：登陆到下单流程
    mvc：mvc接口用例分离示例（不推荐）
    tep：极速写法（强烈推荐）
tests：测试用例
utils：工具
  fastapi_mock.py：自带fastapi项目
  http_client.py：tep request猴子补丁
  mitm.py：mitmproxy抓包自动生成用例
.gitignore：Git忽略文件规则
conf.yaml：项目配置
conftest.py：pytest conftest
pytest.ini：pytest配置
"""

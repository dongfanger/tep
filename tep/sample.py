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

import pytest

# 项目目录路径
_project_dir = os.path.dirname(os.path.abspath(__file__))


# 设置缓存供tep使用
@pytest.fixture(scope="session", autouse=True)
def _project_cache(request):
    request.config.cache.set("project_dir", _project_dir)


# 自动导入fixtures
_fixtures_dir = os.path.join(_project_dir, "fixtures")
for root, _, files in os.walk(_fixtures_dir):
    for file in files:
        if file.startswith("fixture_") and file.endswith(".py"):
            full_path = os.path.join(root, file)
            import_path = full_path.replace(_fixtures_dir, "").replace("\\\\", ".").replace("/", ".").replace(".py", "")
            try:
                fixture_path = "fixtures" + import_path
                exec(f"from {fixture_path} import *")
            except:
                fixture_path = ".fixtures" + import_path
                exec(f"from {fixture_path} import *")
"""

pytest_ini_content = """[pytest]
markers =
    smoke: smoke test
    regress: regress test
"""

fixture_admin_content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Can only be modified by the administrator. Only fixtures are provided.
\"\"\"

from tep.fixture import *


@pytest.fixture
def common_created_by_admin():
    pass
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
            \"qa\": {
                "domain": "http://127.0.0.1:5000",
                "mysql_engine": mysql_engine("127.0.0.1",  # host
                                             "2306",  # port
                                             "root",  # username
                                             "123456",  # password
                                             "qa"),  # db_name
            },
            "release": {
                "domain": "https://release.com",
                "mysql_engine": mysql_engine("127.0.0.1",
                                             "2306",
                                             "root",
                                             "123456",
                                             "release"),
            }
            # 继续添加
        }
        # 定义类属性，敲代码时会有智能提示
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
    # Code your login
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

fixture_your_name_content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Please define your own fixture.
\"\"\"

from tep.fixture import *


@pytest.fixture(scope="session")
def env_vars_your_name(config):
    class Clazz:
        env = config["env"]

        # Environment and variables
        mapping = {
            "qa": {
                "your_var": "123",
            },
            "release": {
                "your_var": "456",
            }
            # Add your environment and variables
        }
        # Define properties for auto display
        your_var = mapping[env]["your_var"]

    return Clazz()


@pytest.fixture
def share_your_name():
    pass
"""

fixture_second_content = """#!/usr/bin/python
# encoding=utf-8


from tep.fixture import *


@pytest.fixture
def fixture_second():
    logger.info("fixture_second")
"""

fixture_three_content = """#!/usr/bin/python
# encoding=utf-8


from tep.fixture import *


@pytest.fixture
def fixture_three():
    logger.info("fixture_three")
"""

test_login_content = """from loguru import logger


def test_login(login):
    logger.info(login.token)
"""

test_post_content = """import jmespath
from loguru import logger

from tep.client import request


def test_post(faker_ch, url, login):
    # description
    logger.info("test post")
    # data
    fake = faker_ch
    # request
    response = request(
        "post",
        url=url("/api/users"),
        headers=login.jwt_headers,
        json={
            "name": fake.name()
        }
    )
    # assert
    assert response.status_code < 400
    # extract
    user_id = jmespath.search("id", response.json())
"""

test_mysql_content = """from loguru import logger
from tep.dao import print_db_table


def test_mysql(pd, env_vars):
    data = pd.read_sql("select 1 from dual", env_vars.mysql_engine)
    logger.info(print_db_table(data))
"""

test_request_content = """from tep.client import request

request("get", url="", headers={}, json={})
request("post", url="", headers={}, params={})
request("put", url="", headers={}, json={})
request("delete", url="", headers={})

# upload excel
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
from tep.client import TepResponse


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
    return TepResponse(response)


def request(method, url, **kwargs):
    client.tep_request_monkey_patch = request_monkey_patch
    return client.request(method, url, **kwargs)
"""

test_login_pay_content = """import jmespath
from tep.client import request

\"\"\"
测试登录到下单流程，需要先运行utils/flask_mock_api.py
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

test_login_pay_httprunner_content = """from httprunner import HttpRunner, Config, Step, RunRequest

\"\"\"
测试登录到下单流程，需要先运行utils/flask_mock_api.py
\"\"\"


class TestLoginPay(HttpRunner):
    config = (
        Config("登录到下单流程")
            .variables(
            **{
                "skuNum": "3"
            }
        )
            .base_url("http://127.0.0.1:5000")
    )

    teststeps = [
        Step(
            RunRequest("登录")
                .post("/login")
                .with_headers(**{"Content-Type": "application/json"})
                .with_json({"username": "dongfanger", "password": "123456"})
                .extract()
                .with_jmespath("body.token", "token")
                .validate()
                .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("搜索商品")
                .get("searchSku?skuName=电子书")
                .with_headers(**{"token": "$token"})
                .extract()
                .with_jmespath("body.skuId", "skuId")
                .with_jmespath("body.price", "skuPrice")
                .validate()
                .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("添加购物车")
                .post("/addCart")
                .with_headers(**{"Content-Type": "application/json",
                                 "token": "$token"})
                .with_json({"skuId": "$skuId", "skuNum": "$skuNum"})
                .extract()
                .with_jmespath("body.totalPrice", "totalPrice")
                .validate()
                .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("下单")
                .post("/order")
                .with_headers(**{"Content-Type": "application/json",
                                 "token": "$token"})
                .with_json({"skuId": "$skuId", "price": "$skuPrice", "skuNum": "$skuNum", "totalPrice": "$totalPrice"})
                .extract()
                .with_jmespath("body.orderId", "orderId")
                .validate()
                .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("支付")
                .post("/pay")
                .with_headers(**{"Content-Type": "application/json",
                                 "token": "$token"})
                .with_json({"orderId": "$orderId", "payAmount": "6.9"})
                .validate()
                .assert_equal("status_code", 200)
                .assert_equal("body.success", "true")
        ),
    ]
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

from services.AddCart import AddCart
from services.Login import Login
from services.Order import Order
from services.Pay import Pay
from services.SearchSku import SearchSku

\"\"\"
测试登录到下单流程，需要先运行utils / flask_mock_api.py
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

test_multi_fixture_content = """#!/usr/bin/python
# encoding=utf-8


def test(fixture_second, fixture_three):
    pass
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

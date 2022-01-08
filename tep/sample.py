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

\"\"\" Can only be modified by the administrator. Only fixtures are provided.
\"\"\"

import os

import pytest

# Initial
_project_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session", autouse=True)
def _project_cache(request):
    request.config.cache.set("project_dir", _project_dir)


# Auto import fixtures
_fixtures_dir = os.path.join(_project_dir, "fixtures")
for root, _, files in os.walk(_fixtures_dir):
    for file in files:
        if os.path.isfile(os.path.join(root, file)):
            if file.startswith("fixture_") and file.endswith(".py"):
                _fixture_name, _ = os.path.splitext(file)
                try:
                    exec(f"from fixtures.{_fixture_name} import *")
                except:
                    pass
                try:
                    exec(f"from .fixtures.{_fixture_name} import *")
                except:
                    pass
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

        \"\"\"Variables define start\"\"\"
        # Environment and variables
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
            # Add your environment and variables
        }
        # Define properties for auto display
        domain = mapping[env]["domain"]
        mysql_engine = mapping[env]["mysql_engine"]
        \"\"\"Variables define end\"\"\"

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

flask_mock_api_content = """#!/usr/bin/python
# encoding=utf-8

import json

from flask import Flask, request

# Flask实例
app = Flask(__name__)


def is_headers_equal(headers, data):
    # 简单比较请求头是否一致
    for k, v in data.items():
        if headers.get(k) != v:
            return False
    return True


def is_args_equal(args, data):
    # 简单比较请求参数是否一致
    for k, v in data.items():
        if args.get(k) != v:
            return False
    return True


def is_json_equal(json_, data):
    # 简单比较请求体是否一致
    json_ = json.loads(json_)
    for k, v in data.items():
        if json_.get(k) != v:
            return False
    return True


@app.route("/login", methods=["POST"])
def login():
    if is_json_equal(request.get_data(), {"username": "dongfanger", "password": "123456"}):
        return {"token": "de2e3ffu29"}
    return "", 500


@app.route("/searchSku")
def search_sku():
    if is_headers_equal(request.headers, {"token": "de2e3ffu29"}) and is_args_equal(request.args, {"skuName": "电子书"}):
        return {"skuId": "222", "price": "2.3"}
    return "", 500


@app.route("/addCart", methods=["POST"])
def add_cart():
    if is_headers_equal(request.headers, {"token": "de2e3ffu29"}) and is_json_equal(request.get_data(),
                                                                                    {"skuId": "222", "skuNum": "3"}):
        return {"skuId": "222", "price": "2.3", "skuNum": "3", "totalPrice": "6.9"}
    return "", 500


@app.route("/order", methods=["POST"])
def order():
    if is_headers_equal(request.headers, {"token": "de2e3ffu29"}) and is_json_equal(request.get_data(),
                                                                                    {"skuId": "222", "price": "2.3",
                                                                                     "skuNum": "3",
                                                                                     "totalPrice": "6.9"}):
        return {"orderId": "333"}
    return "", 500


@app.route("/pay", methods=["GET", "POST"])
def pay():
    if is_headers_equal(request.headers, {"token": "de2e3ffu29"}) and is_json_equal(request.get_data(),
                                                                                    {"orderId": "333",
                                                                                     "payAmount": "6.9"}):
        return {"success": "true"}
    return "", 500


if __name__ == "__main__":
    app.run()
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

SearchSku_content = """from services.http.base import BaseRequest


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

test_login_pay_mvc_content = """import allure
from tep.fixture import TepVars

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

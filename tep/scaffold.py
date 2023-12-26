#!/usr/bin/python
# encoding=utf-8

import os
import platform
import sys

import logging

from tep.libraries.Config import Config


def init_parser_scaffold(subparsers):
    sub_parser_scaffold = subparsers.add_parser("new", help="Create a new project with template structure.")
    sub_parser_scaffold.add_argument("project_name", type=str, nargs="?", help="Specify new project name.")
    sub_parser_scaffold.add_argument(
        "-venv",
        dest="create_venv",
        action="store_true",
        help="Create virtual environment in the project, and install tep.",
    )
    return sub_parser_scaffold


def scaffold(args):
    Config.CREATE_ENV = args.create_venv
    sys.exit(create_scaffold(args.project_name))


def create_scaffold(project_name):
    if os.path.isdir(project_name):
        logging.warning(f"Project folder {project_name} exists, please specify a new project name")
        return 1
    elif os.path.isfile(project_name):
        logging.warning(f"Project name {project_name} conflicts with existed file, please specify a new one")
        return 1

    print(f"Create new project: {project_name}")
    print(f"Project root dir: {os.path.join(os.getcwd(), project_name)}\n")

    def create_folder(path):
        os.makedirs(path)
        msg = f"Created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"Created file:   {path}"
        print(msg)

    create_folder(project_name)
    create_folder(os.path.join(project_name, "case"))
    create_folder(os.path.join(project_name, "case", "场景测试"))
    create_folder(os.path.join(project_name, "data"))
    create_folder(os.path.join(project_name, "data", "har"))
    create_folder(os.path.join(project_name, "fixture"))
    create_folder(os.path.join(project_name, "report"))
    create_folder(os.path.join(project_name, "util"))

    replay_content = """import os

from tep.libraries.Config import Config
from tep.libraries.Har import Har

if __name__ == '__main__':
    profile = {
        "harDir": os.path.join(Config.BASE_DIR, "data", "har"),
        "desDir": os.path.join(Config.BASE_DIR, "case", "replay")
    }
    Har(profile).har2case()
"""
    create_file(os.path.join(project_name, "replay.py"), replay_content)
    run_content = """from tep.libraries.Run import Run

if __name__ == '__main__':
    settings = {
        "path": ["示例.py"],  # Path to run, relative path to case
        "report": False  # Output test report or not
    }
    Run(settings)
"""
    create_file(os.path.join(project_name, "run.py"), run_content)
    conftest_content = """from tep.plugin import tep_plugins

pytest_plugins = tep_plugins()
"""
    create_file(os.path.join(project_name, "conftest.py"), conftest_content)
    ini_content = """[pytest]
python_files = *.py
log_cli = True
log_level = INFO
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S"""
    create_file(os.path.join(project_name, "pytest.ini"), ini_content)
    gitignore_content = """.idea
.pytest_cache/
__pycache__/
.har
"""
    create_file(os.path.join(project_name, ".gitignore"), gitignore_content)
    create_file(os.path.join(project_name, "case", "__init__.py"), "")
    demo_content = """def test(HTTPRequestKeyword):
    response = HTTPRequestKeyword("get", url="http://httpbin.org/status/200")
    assert response.status_code == 200
"""
    create_file(os.path.join(project_name, "case", "示例.py"), demo_content)
    flow_content = """def test(HTTPRequestKeyword, JSONKeyword, VarKeyword, login, StringKeyword):
    headers = login()
    var = VarKeyword({
        "domain": "http://127.0.0.1:5000",
        "headers": headers
    })

    url = StringKeyword("${domain}/searchSku?skuName=book")
    response = HTTPRequestKeyword("get", url=url, headers=var["headers"])
    assert response.status_code < 400
    var["skuId"] = response.jsonpath("$.skuId")
    var["skuPrice"] = response.jsonpath("$.price")

    url = StringKeyword("${domain}/addCart")
    body = JSONKeyword(r\"\"\"
{
    "skuId":"${skuId}",
    "skuNum":2
}
\"\"\")
    response = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert response.status_code < 400
    var["skuNum"] = response.jsonpath("$.skuNum")
    var["totalPrice"] = response.jsonpath("$.totalPrice")

    url = StringKeyword("${domain}/order")
    body = JSONKeyword(r\"\"\"
{
    "skuId":"${skuId}",
    "price":${skuPrice},
    "skuNum":${skuNum},
    "totalPrice":${totalPrice}
}
\"\"\")
    response = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert response.status_code < 400
    var["orderId"] = response.jsonpath("$.orderId")

    url = StringKeyword("${domain}/pay")
    body = JSONKeyword(r\"\"\"
{
    "orderId":"${orderId}",
    "payAmount":"0.2"
}
\"\"\")
    response = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert response.status_code < 400
    assert response.jsonpath("$.success") == "true"
"""
    create_file(os.path.join(project_name, "case", "场景测试", "登录-商品-购物车-下单-支付.py"), flow_content)
    mock_content = """import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/login")
async def login(req: Request):
    body = await req.json()
    if body["username"] == "dongfanger" and body["password"] == "123456":
        return {"Cookie": "de2e3ffu29"}
    return ""


@app.get("/searchSku")
async def search_sku(req: Request):
    if req.headers.get("Cookie") == "de2e3ffu29" and req.query_params.get("skuName") == "book":
        return {"skuId": "222", "price": "2.3"}
    return ""


@app.post("/addCart")
async def add_cart(req: Request):
    body = await req.json()
    if req.headers.get("Cookie") == "de2e3ffu29" and body["skuId"] == "222":
        return {"skuId": "222", "price": "2.3", "skuNum": 3, "totalPrice": "6.9"}
    return ""


@app.post("/order")
async def order(req: Request):
    body = await req.json()
    if req.headers.get("Cookie") == "de2e3ffu29" and body["skuId"] == "222":
        return {"orderId": "333"}
    return ""


@app.post("/pay")
async def pay(req: Request):
    body = await req.json()
    if req.headers.get("Cookie") == "de2e3ffu29" and body["orderId"] == "333":
        return {"success": "true"}
    return ""


@app.get("/retry/code", status_code=500)
async def retry_code(req: Request):
    return {"success": "false"}


if __name__ == '__main__':
    uvicorn.run("mock:app", host="127.0.0.1", port=5000)
"""
    create_file(os.path.join(project_name, "util", "mock.py"), mock_content)
    login_content = """import pytest


@pytest.fixture(scope="session")
def login(HTTPRequestKeyword):
    def _function():
        url = "http://127.0.0.1:5000/login"
        headers = {"Content-Type": "application/json"}
        body = {"username": "dongfanger", "password": "123456"}
        response = HTTPRequestKeyword("post", url=url, headers=headers, json=body)
        assert response.status_code < 400
        return {"Content-Type": "application/json", "Cookie": f"{response.json()['Cookie']}"}

    return _function
"""
    create_file(os.path.join(project_name, "fixture", "fixture_login.py"), login_content)
    user_defined_variables_content = 'name: "公众号测试开发刚哥"'
    create_file(os.path.join(project_name, "data", "UserDefinedVariables.yaml"), user_defined_variables_content)

    if Config.CREATE_ENV:
        # Create Python virtual Environment
        os.chdir(project_name)
        print("\nCreating virtual environment")
        os.system("python -m venv .venv")
        print("Created virtual environment: .venv")

        # Install tep in the Python virtual Environment
        print("Installing tep")
        if platform.system().lower() == 'windows':
            os.chdir(".venv")
            os.chdir("Scripts")
            os.system("pip install tep")
        elif platform.system().lower() == 'linux':
            os.chdir(".venv")
            os.chdir("bin")
            os.system("pip install tep")

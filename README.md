# tep

`tep`是**T**ry **E**asy **P**ytest的首字母缩写，是一款基于pytest测试框架的测试工具，集成了各种实用的第三方包和优秀的自动化测试设计思想，帮你快速实现自动化项目落地。

# 安装

支持Python3.6以上，推荐Python3.8以上。

标准安装：

```
$ pip install tep
```

国内镜像：

```
$ pip --default-timeout=600 install -i https://pypi.tuna.tsinghua.edu.cn/simple tep
```

检查安装成功：

```
$ tep -V  # 或者 tep --version
0.2.3
```

# 快速创建项目

tep提供了脚手架，预置了项目结构和代码，打开cmd，使用`startproject`命令快速创建项目：

```
tep startproject project_name
```

并且提供了`-venv`参数，在项目初始化时，可以同时创建一个虚拟环境（推荐）：

```
tep startproject project_name -venv
```

# 输出测试报告

tep提供了`--tep-reports`参数来生成allure测试报告：

```
pytest  --tep-reports
```

报告文件存放在根目录的`reports/`中。

# Mock服务

tep自带了一个Flask应用（`utils/flask_mock_api.py`），提供了登录到下单流程的5个接口，启动后即可一键运行示例中的测试用例。

# 三种开发模式

tep兼容三种开发模式：用例数据一体（适合新手）、用例数据分离（适合老手）、HttpRunner（新老皆宜）。

①用例数据一体，示例代码如下所示：

```python
import jmespath
from tep.client import request


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
        json={"skuId": sku_id, "skuNum": sku_num}
    )
    total_price = jmespath.search("totalPrice", response.json())
    assert response.status_code < 400

    # 下单
    response = request(
        "post",
        url=env_vars.domain + "/order",
        headers={"token": login.token},
        json={"skuId": sku_id, "price": sku_price, "skuNum": sku_num, "totalPrice": total_price}
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

```

更多内容请参考[《如何使用teprunner测试平台编写从登录到下单的大流程接口自动化用例》](https://dongfanger.gitee.io/blog/teprunner/012-%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8teprunner%E6%B5%8B%E8%AF%95%E5%B9%B3%E5%8F%B0%E7%BC%96%E5%86%99%E4%BB%8E%E7%99%BB%E5%BD%95%E5%88%B0%E4%B8%8B%E5%8D%95%E7%9A%84%E5%A4%A7%E6%B5%81%E7%A8%8B%E6%8E%A5%E5%8F%A3%E8%87%AA%E5%8A%A8%E5%8C%96%E7%94%A8%E4%BE%8B.html)

②用例数据分离

开发中，敬请期待...
③HttpRunner，示例代码如下所示：

```python
from httprunner import HttpRunner, Config, Step, RunRequest


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
```

# 用户手册

https://dongfanger.gitee.io/blog/chapters/tep.html

# 联系我

https://dongfanger.gitee.io/blog/more.html


# 简介

tep是Try Easy Pytest的首字母缩写，帮你轻松上手pytest。

框架特点：

- 基于pytest封装，成熟、稳定且扩展性强。
- 框架完全由Python构建，没有混杂其他语言。
- 原生Python语法，学习Python，零成本使用框架。
- HAR包转换pytest用例。
- 函数v()支持${}占位符语法，便捷管理接口数据。

# 安装

支持Python3.8以上版本

创建虚拟环境：`python -m venv .venv`

激活虚拟环境，Windows用户：`activate.bat` Mac用户：`source .venv/bin/activate`

安装tep：`pip install tep`

验证安装成功：`tep -V`

用例示范：

```python
import json

from tep import request
from tep import step
from tep import v

from data.global_data import GlobalData


def test():
    v({
        "domain": GlobalData.domain,
        "skuNum": 2,
        "payAmount": 0.2
    })

    step("查询商品", step_search_sku)
    step("添加购物车", step_add_cart)
    step("下单", step_order)
    step("支付", step_pay)


def step_search_sku():
    url = v("${domain}/searchSku?skuName=book")
    response = request("get", url=url, headers=GlobalData.headers)
    assert response.status_code < 400
    v("skuId", response.jsonpath("$.skuId")[0])
    v("skuPrice", response.jsonpath("$.price")[0])


def step_add_cart():
    url = v("${domain}/addCart")
    body = """
{
    "skuId": "${skuId}",
    "skuNum":${skuNum}
}
"""
    response = request("post", url=url, headers=GlobalData.headers, json=json.loads(v(body)))
    assert response.status_code < 400
    v("skuNum", response.jsonpath("$.skuNum")[0])
    v("totalPrice", response.jsonpath("$.totalPrice")[0])


def step_order():
    url = v("${domain}/order")
    body = """
{
    "skuId": "${skuId}",
    "price":${skuPrice},
    "skuNum":${skuNum},
    "totalPrice":${totalPrice}
}
"""
    response = request("post", url=url, headers=GlobalData.headers, json=json.loads(v(body)))
    assert response.status_code < 400
    v("orderId", response.jsonpath("$.orderId")[0])


def step_pay():
    url = v("${domain}/pay")
    body = """
{
    "orderId": "${orderId}",
    "payAmount":${payAmount}
}
"""
    response = request("post", url=url, headers=GlobalData.headers, json=json.loads(v(body)))
    assert response.status_code < 400
    assert response.jsonpath("$.success")[0] == "true"
```

# 更多介绍

[原创接口测试框架tep](https://dongfanger.github.io/chapters/%E5%8E%9F%E5%88%9B%E6%8E%A5%E5%8F%A3%E6%B5%8B%E8%AF%95%E6%A1%86%E6%9E%B6tep.html)

# 重要版本说明

- V3.0.0 纯粹Python接口测试框架
- V2.0.0 关键字驱动框架
- V1.0.0 tep小工具完整教程
- V0.2.3 tep小工具首次开源
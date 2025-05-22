import json

from tep import request
from tep import step
from tep import v

from data.GlobalData import GlobalData


def test():
    v({
        'domain': GlobalData.domain,
        'skuNum': 2,
        'payAmount': 0.2
    })

    step('查询商品', step_search_sku)
    step('添加购物车', step_add_cart)
    step('下单', step_order)
    step('支付', step_pay)


def step_search_sku():
    url = v('${domain}/searchSku?skuName=book')
    response = request('get', url=url, headers=GlobalData.headers)
    assert response.status_code < 400
    v('skuId', response.jsonpath('$.skuId')[0])
    v('skuPrice', response.jsonpath('$.price')[0])


def step_add_cart():
    url = v('${domain}/addCart')
    body = '''
{
    "skuId": "${skuId}",
    "skuNum":${skuNum}
}
'''
    response = request('post', url=url, headers=GlobalData.headers, json=json.loads(v(body)))
    assert response.status_code < 400
    v('skuNum', response.jsonpath('$.skuNum')[0])
    v('totalPrice', response.jsonpath('$.totalPrice')[0])


def step_order():
    url = v('${domain}/order')
    body = '''
{
    "skuId": "${skuId}",
    "price":${skuPrice},
    "skuNum":${skuNum},
    "totalPrice":${totalPrice}
}
'''
    response = request('post', url=url, headers=GlobalData.headers, json=json.loads(v(body)))
    assert response.status_code < 400
    v('orderId', response.jsonpath('$.orderId')[0])


def step_pay():
    url = v('${domain}/pay')
    body = '''
{
    "orderId": "${orderId}",
    "payAmount":${payAmount}
}
'''
    response = request('post', url=url, headers=GlobalData.headers, json=json.loads(v(body)))
    assert response.status_code < 400
    assert response.jsonpath('$.success')[0] == 'true'

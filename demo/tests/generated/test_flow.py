from tep import request
from tep import v


class Data:
    v({"domain": "http://127.0.0.1:5000"})
    headers = {'Content-Type': 'application/json', 'Cookie': 'de2e3ffu29'}
    body_1 = '{"username":"dongfanger","password":"123456"}'
    body_2 = '{"skuId":"222","skuNum":2}'
    body_3 = '{"skuId":"222","price":2.3,"skuNum":3,"totalPrice":6.9}'
    body_4 = '{"orderId":"333","payAmount":"0.2"}'


def test():

    url = v('${domain}/login')
    body = v(Data.body_1)
    response = request('post', url=url, headers=Data.headers, json=body)
    # v('name', response.jsonpath('$.jsonpath')[0])
    assert response.status_code < 400
    
    url = v('${domain}/searchSku?skuName=book')
    response = request('get', url=url, headers=Data.headers)
    # v('name', response.jsonpath('$.jsonpath')[0])
    assert response.status_code < 400
    
    url = v('${domain}/addCart')
    body = v(Data.body_2)
    response = request('post', url=url, headers=Data.headers, json=body)
    # v('name', response.jsonpath('$.jsonpath')[0])
    assert response.status_code < 400
    
    url = v('${domain}/order')
    body = v(Data.body_3)
    response = request('post', url=url, headers=Data.headers, json=body)
    # v('name', response.jsonpath('$.jsonpath')[0])
    assert response.status_code < 400
    
    url = v('${domain}/pay')
    body = v(Data.body_4)
    response = request('post', url=url, headers=Data.headers, json=body)
    # v('name', response.jsonpath('$.jsonpath')[0])
    assert response.status_code < 400

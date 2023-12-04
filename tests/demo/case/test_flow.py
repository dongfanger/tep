def test(HTTPRequestKeyword, JSONKeyword, login):
    headers = login()
    var = {"domain": "http://127.0.0.1:5000", "headers": headers}

    url = var["domain"] + "/searchSku" + "?skuName=book"
    response = HTTPRequestKeyword("get", url=url, headers=var["headers"])
    assert response.status_code < 400
    sku_id = response.jsonpath("$.skuId")
    sku_price = response.jsonpath("$.price")

    url = var["domain"] + "/addCart"
    body = r"""{"skuId":1,"skuNum":2}"""
    body = JSONKeyword(body, {"$.skuId": sku_id})
    response = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert response.status_code < 400
    sku_num = response.jsonpath("$.skuNum")
    total_price = response.jsonpath("$.totalPrice")

    url = var["domain"] + "/order"
    body = r"""{"skuId":1,"price":2,"skuNum":3,"totalPrice":4}"""
    body = JSONKeyword(body, {"$.skuId": sku_id, "$.price": sku_price, "$.skuNum": sku_num, "$.totalPrice": total_price})
    response = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert response.status_code < 400
    order_id = response.jsonpath("$.orderId")

    url = var["domain"] + "/pay"
    body = r"""{"orderId":1,"payAmount":"0.2"}"""
    body = JSONKeyword(body, {"$.orderId": order_id})
    response = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert response.status_code < 400
    assert response.jsonpath("$.success") == "true"

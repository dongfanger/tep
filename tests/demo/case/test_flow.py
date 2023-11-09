def test(HTTPRequestKeyword, BodyKeyword, login):
    ro = login()
    var = {"domain": "http://127.0.0.1:5000", "headers": ro.data}

    url = var["domain"] + "/searchSku" + "?skuName=book"
    ro = HTTPRequestKeyword("get", url=url, headers=var["headers"])
    assert ro.response.status_code < 400
    sku_id = ro.response.jsonpath("$.skuId")
    sku_price = ro.response.jsonpath("$.price")

    url = var["domain"] + "/addCart"
    body = r"""{"skuId":1,"skuNum":2}"""
    ro = BodyKeyword(body, {"$.skuId": sku_id})
    body = ro.data
    ro = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert ro.response.status_code < 400
    sku_num = ro.response.jsonpath("$.skuNum")
    total_price = ro.response.jsonpath("$.totalPrice")

    url = var["domain"] + "/order"
    body = r"""{"skuId":1,"price":2,"skuNum":3,"totalPrice":4}"""
    ro = BodyKeyword(body, {"$.skuId": sku_id, "$.price": sku_price, "$.skuNum": sku_num, "$.totalPrice": total_price})
    body = ro.data
    ro = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert ro.response.status_code < 400
    order_id = ro.response.jsonpath("$.orderId")

    url = var["domain"] + "/pay"
    body = r"""{"orderId":1,"payAmount":"0.2"}"""
    ro = BodyKeyword(body, {"$.orderId": order_id})
    body = ro.data
    ro = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert ro.response.status_code < 400
    assert ro.response.jsonpath("$.success") == "true"

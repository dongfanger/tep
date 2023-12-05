def test(HTTPRequestKeyword, JSONKeyword, VarKeyword, login):
    headers = login()
    var = VarKeyword({
        "domain": "http://127.0.0.1:5000",
        "headers": headers
    })

    url = var["domain"] + "/searchSku" + "?skuName=book"
    response = HTTPRequestKeyword("get", url=url, headers=var["headers"])
    assert response.status_code < 400
    var["skuId"] = response.jsonpath("$.skuId")
    var["skuPrice"] = response.jsonpath("$.price")

    url = var["domain"] + "/addCart"
    body = JSONKeyword(r"""
{
    "skuId":"${skuId}",
    "skuNum":2
}
""")
    response = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert response.status_code < 400
    var["skuNum"] = response.jsonpath("$.skuNum")
    var["totalPrice"] = response.jsonpath("$.totalPrice")

    url = var["domain"] + "/order"
    body = JSONKeyword(r"""
{
    "skuId":"${skuId}",
    "price":${skuPrice},
    "skuNum":${skuNum},
    "totalPrice":${totalPrice}
}
""")
    response = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert response.status_code < 400
    var["orderId"] = response.jsonpath("$.orderId")

    url = var["domain"] + "/pay"
    body = JSONKeyword(r"""
{
    "orderId":"${orderId}",
    "payAmount":"0.2"
}
""")
    response = HTTPRequestKeyword("post", url=url, headers=var["headers"], json=body)
    assert response.status_code < 400
    assert response.jsonpath("$.success") == "true"

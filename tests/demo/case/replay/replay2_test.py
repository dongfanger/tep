def test(HTTPRequestKeyword, BodyKeyword):
    var = {}
    
    url = "http://httpbin.org/status/200"
    headers = {'Host': 'httpbin.org', 'Connection': 'keep-alive', 'accept': 'text/plain', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'Referer': 'http://httpbin.org/', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    ro = HTTPRequestKeyword("get", url=url, headers=headers)
    # user_defined_var = ro.response.jsonpath("$.jsonpath")
    assert ro.response.status_code < 400

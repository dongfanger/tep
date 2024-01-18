def test(HTTPRequestKeyword, JSONKeyword, VarKeyword):
    var = VarKeyword({})
    
    url = "https://postman-echo.com/get?foo1=HDnY8&foo2=34.5"
    headers = JSONKeyword(r"""
{
    "Host":"postman-echo.com",
    "User-Agent":"HttpRunnerPlus",
    "Accept-Encoding":"gzip"
}
""")
    response = HTTPRequestKeyword("get", url=url, headers=headers)
    # user_defined_var = response.jsonpath("$.jsonpath")
    assert response.status_code < 400
    
    url = "https://postman-echo.com/post"
    headers = JSONKeyword(r"""
{
    "Host":"postman-echo.com",
    "User-Agent":"Go-http-client/1.1",
    "Content-Length":"28",
    "Content-Type":"application/json; charset=UTF-8",
    "Cookie":"sails.sid=s%3Az_LpglkKxTvJ_eHVUH6V67drKp0AGWW-.PidabaXOnatLRP47hVyqqepl6BdrpEQzRlJQXtbIiwk",
    "Accept-Encoding":"gzip",
    "sails.sid":"s%3Az_LpglkKxTvJ_eHVUH6V67drKp0AGWW-.PidabaXOnatLRP47hVyqqepl6BdrpEQzRlJQXtbIiwk"
}
""")
    body = JSONKeyword(r"""
{
    "foo1":"HDnY8",
    "foo2":12.3
}
""")
    response = HTTPRequestKeyword("post", url=url, headers=headers, json=body)
    # user_defined_var = response.jsonpath("$.jsonpath")
    assert response.status_code < 400
    
    url = "https://postman-echo.com/post"
    headers = JSONKeyword(r"""
{
    "Host":"postman-echo.com",
    "User-Agent":"Go-http-client/1.1",
    "Content-Length":"20",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":"sails.sid=s%3AS5e7w0zQ0xAsCwh9L8T6R7QLYCO7_gtD.r8%2B2w9IWqEIfuVkrZjnxzm2xADIk34zKAWXRPapr%2FAw",
    "Accept-Encoding":"gzip",
    "sails.sid":"s%3AS5e7w0zQ0xAsCwh9L8T6R7QLYCO7_gtD.r8%2B2w9IWqEIfuVkrZjnxzm2xADIk34zKAWXRPapr%2FAw"
}
""")
    response = HTTPRequestKeyword("post", url=url, headers=headers, data=body)
    # user_defined_var = response.jsonpath("$.jsonpath")
    assert response.status_code < 400

from tep.libraries.Diff import Diff
from tep.libraries.Sqlite import Sqlite


def test(HTTPRequestKeyword, BodyKeyword):
    var = {'caseId': '023f387db398504889e0afb8dd1bc99d', 'requestOrder': 1, 'diffDir': '/Users/wanggang424/Desktop/PycharmProjects/tep/tests/demo/case/har/demo-replay-diff'}
    
    url = "https://postman-echo.com/get?foo1=HDnY8&foo2=34.5"
    headers = {'Host': 'postman-echo.com', 'User-Agent': 'HttpRunnerPlus', 'Accept-Encoding': 'gzip'}
    ro = HTTPRequestKeyword("get", url=url, headers=headers)
    # user_defined_var = ro.response.jsonpath("$.jsonpath")
    assert ro.response.status_code < 400
    Sqlite.record_actual((ro.response.text, var["caseId"], var["requestOrder"], "GET", "https://postman-echo.com/get?foo1=HDnY8&foo2=34.5"), var)
    
    url = "https://postman-echo.com/post"
    headers = {'Host': 'postman-echo.com', 'User-Agent': 'Go-http-client/1.1', 'Content-Length': '28', 'Content-Type': 'application/json; charset=UTF-8', 'Cookie': 'sails.sid=s%3Az_LpglkKxTvJ_eHVUH6V67drKp0AGWW-.PidabaXOnatLRP47hVyqqepl6BdrpEQzRlJQXtbIiwk', 'Accept-Encoding': 'gzip', 'sails.sid': 's%3Az_LpglkKxTvJ_eHVUH6V67drKp0AGWW-.PidabaXOnatLRP47hVyqqepl6BdrpEQzRlJQXtbIiwk'}
    body = r"""{"foo1":"HDnY8","foo2":12.3}"""
    ro = BodyKeyword(body)
    # ro = BodyKeyword(body, {"$.jsonpath": "value"})
    body = ro.data
    ro = HTTPRequestKeyword("post", url=url, headers=headers, json=body)
    # user_defined_var = ro.response.jsonpath("$.jsonpath")
    assert ro.response.status_code < 400
    Sqlite.record_actual((ro.response.text, var["caseId"], var["requestOrder"], "POST", "https://postman-echo.com/post"), var)
    
    url = "https://postman-echo.com/post"
    headers = {'Host': 'postman-echo.com', 'User-Agent': 'Go-http-client/1.1', 'Content-Length': '20', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'sails.sid=s%3AS5e7w0zQ0xAsCwh9L8T6R7QLYCO7_gtD.r8%2B2w9IWqEIfuVkrZjnxzm2xADIk34zKAWXRPapr%2FAw', 'Accept-Encoding': 'gzip', 'sails.sid': 's%3AS5e7w0zQ0xAsCwh9L8T6R7QLYCO7_gtD.r8%2B2w9IWqEIfuVkrZjnxzm2xADIk34zKAWXRPapr%2FAw'}
    ro = HTTPRequestKeyword("post", url=url, headers=headers, data=body)
    # user_defined_var = ro.response.jsonpath("$.jsonpath")
    assert ro.response.status_code < 400
    Sqlite.record_actual((ro.response.text, var["caseId"], var["requestOrder"], "POST", "https://postman-echo.com/post"), var)

    Diff.make(var["caseId"], var["diffDir"])

![Snip20231106_197](https://github.com/dongfanger/tep/assets/44184507/459c9254-6fe6-41ab-a752-a77408d0bb04)

# **tep简介**

`tep`是**T**ry **E**asy **P**ytest的首字母缩写，关键字驱动框架，专注于接口自动化测试，单个文件即可完成用例编写。

# 设计理念

✔️稳定：基于成熟框架pytest，天生强大

✔️规范：RobotFramework风格，井井有条

✔️统一：关键字命名与JMeter组件一致，一知万用

✔️原生：关键字用法保留Python原生定义，轻车熟路

✔️兼容：分层机制保证迭代升级不影响老项目，向下兼容

❌拒绝低代码平台，开发成本太高。

❌拒绝EXCEL/YAML，调试太麻烦。

❌拒绝深度编程，绕来绕去太复杂。

✌️只需要一点点Python基础，就能轻松搞定接口自动化。

# **快速入门**

## **安装**

```Shell
pip install tep
```

验证安装成功：

```Shell
tep -v
```

```Plain
Current Version: V2.0.0

 ____o__ __o____   o__ __o__/_   o__ __o
  /   \   /   \   <|    v       <|     v\
       \o/        < >           / \     <\
        |          |            \o/     o/
       < >         o__/_         |__  _<|/
        |          |             |
        o         <o>           <o>
       <|          |             |
       / \        / \  _\o__/_  / \

```

## **新建项目**

```Shell
tep -s demo
```

```Plain
Created folder: demo
Created folder: demo/case
Created folder: demo/data
Created folder: demo/report
Created file:   demo/run.py
Created file:   demo/conftest.py
Created file:   demo/pytest.ini
Created file:   demo/.gitignore.py
Created file:   demo/case/__init__.py
Created file:   demo/case/test_demo.py
Created file:   demo/data/UserDefinedVariables.yaml
```

## 编写用例

在`case/test_demo.py`编写用例，脚手架已自动生成：

```Python
def test(HTTPRequestKeyword):
    ro = HTTPRequestKeyword("get", url="http://httpbin.org/status/200")
    assert ro.response.status_code == 200
```

执行`run.py`后出现以下日志：

```Plain
URL: http://httpbin.org/status/200
Method: GET
Headers: {"User-Agent": "python-requests/2.31.0", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "keep-alive"}
Request Body: None
Status Code: 200
Response Body: 
Elapsed: 0.61046s
```

恭喜您，上手成功！

在线文档，用户手册，请戳链接访问：

[【原创】tep关键字驱动框架教程](https://eqgvpqzl6c.feishu.cn/docx/DZVed7YptocKE1xYIgici1DynTe)

如果对您有所帮助，请帮忙给开源项目点个Star吧，感谢您的支持！

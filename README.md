# tep

tep is a testing tool to help you write pytest more easily. Try Easy Pytest!

[pytest封神之路第零步 快速入门](https://www.cnblogs.com/df888/p/13733877.html)

[pytest封神之路第一步 tep介绍](https://www.cnblogs.com/df888/p/13531714.html)

[pytest封神之路第二步 132个命令行参数用法](https://www.cnblogs.com/df888/p/13649543.html)

[pytest封神之路第三步 精通fixture](https://www.cnblogs.com/df888/p/13691820.html)

[pytest封神之路第四步 内置和自定义marker](https://www.cnblogs.com/df888/p/13715187.html)

[pytest封神之路第五步 参数化进阶](https://www.cnblogs.com/df888/p/13721501.html)

[pytest封神之路第六步 断言技巧](https://www.cnblogs.com/df888/p/13735063.html)

持续更新中...

# Design Philosophy

- Simple is better
- Everyone can write automation in python

# Installation

`tep` is developed with Python, it supports Python `3.6+` and most operating systems.

`tep` is available on [`PyPI`](https://pypi.python.org/pypi) and can be installed through `pip`.

```
$ pip install tep
```

or domestic mirror.

```
$ pip --default-timeout=600 install -i https://pypi.tuna.tsinghua.edu.cn/simple tep
```

# Check Installation

When tep is installed, tep command will be added in your system.

To see `tep` version:

```
$ tep -V  # tep --version
0.2.3
```

# Scaffold

If you want to create a new project, you can use the scaffold to startup quickly.

The only argument you need to specify is the project name.

```
$ tep startproject demo
2020-07-28 14:34:57.649 | INFO     | tep.scaffold:create_scaffold:40 - create new project: demo
project root dir: \PycharmProjects\demo

created folder: demo
created folder: demo\tests
created file: demo\tests\__init__.py
created file: demo\conftest.py
created file: demo\.gitignore

```

The directory looks like this.

```
│  .gitignore
│  conftest.py
└─tests
        __init__.py
```

# Usage

If you want to know more usages, you can read [pytest docs](https://docs.pytest.org/).

You know pytest.

You know tep.

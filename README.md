# tep

tep is a testing tool to help you write pytest more easily. Try Easy Pytest!

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
created folder: demo\testcases
created folder: demo\datafiles
created folder: demo\reports
created file: demo\testcases\__init__.py
created file: demo\testcases\conftest.py
created file: demo\testcases\crud_test.py
created file: demo\run.py
created file: demo\conftest.py
created file: demo\.gitignore

```

The directory looks like this.

```
│  .gitignore
│  conftest.py
│  run.py
│
├─datafiles
├─reports
└─testcases
        conftest.py
        crud_test.py
        __init__.py
```

# Usage

If you want to know more usages, you can read [pytest docs](https://docs.pytest.org/).

You know pytest.

You know tep.
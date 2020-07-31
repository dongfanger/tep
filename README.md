# tep

Try Easy Pytest

## Design Philosophy

- Simple is better
- Inspired by JMeter's design
- Embrace open source, leverage [`pytest`](https://docs.pytest.org/), [`requests`](http://docs.python-requests.org/en/master/), [`faker`](https://faker.readthedocs.io/), [`jmespath`](https://jmespath.org/) and [`allure`](https://docs.qameta.io/allure/).

## Key Features

- With [`pytest`](https://docs.pytest.org/), hundreds of plugins are readily available.
- Inherit all powerful features of [`requests`](http://docs.python-requests.org/en/master/), stay native and strong.
- With [`faker`](https://faker.readthedocs.io/), generate fake data for you. 
- With [`jmespath`](https://jmespath.org/), extract and validate json response has never been easier.
- With [`allure`](https://docs.qameta.io/allure/), test report can be pretty nice and powerful.
- CLI command supported, perfect combination with `CI/CD`.

## Installation

`tep` is developed with Python, it supports Python `3.6+` and most operating systems.

`tep` is available on [`PyPI`](https://pypi.python.org/pypi) and can be installed through `pip`.

```
$ pip install tep
```

If you want to keep up with the latest version, you can install with github repository url.

```
$ pip install git+https://github.com/dongfanger/tep.git@master
```

If you have installed `tep` before and want to upgrade to the latest version, you can use the `-U` option.

```
$ pip install -U tep
$ pip install -U git+https://github.com/dongfanger/tep.git@master
```

## Check Installation

When tep is installed, tep command will be added in your system.

To see `tep` version:

```
$ tep -V  # tep --version
0.2.3
```

To see available options, run:

```
$ tep -h
usage: tep [-h] [-V] {startproject} ...

A RESTful API testing tool inspired by JMeter's design.

positional arguments:
  {startproject}  sub-command help
    startproject  create a new project with template structure.

optional arguments:
  -h, --help      show this help message and exit
  -V, --version   show version
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

# Demo

After the project is created, you can read demo at `testcases\conftest.py` and `testcases\crud_test.py`.

If you want to know more usages, you can read [pytest docs](https://docs.pytest.org/).

You know pytest.

You know tep.
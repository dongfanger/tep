# tep

`tep` is a testing tool to help you write pytest more easily. Try Easy Pytest!

# Design Philosophy

- Simple is better
- Ready is better
- Fast is better

# Key Features

- Inherit all features of `requests`，what `tep.client.request` adds is just a little log.
- A single parameter `--tep-reports` generates the allure html test report.
- Integrate common packages such as `faker`, `jmespath`, `loguru`, `pytest-xdist`, `pytest-assume`.
- Provide a `requirements.txt` that contains some extension packages for optional manual installation.
- The `fixtures` directory is automatically imported by `conftest.py`.

# Installation

`tep` is developed with Python, it supports Python `3.6+` and most operating systems.

`tep` is available on [`PyPI`](https://pypi.python.org/pypi) and can be installed through `pip`:

```
$ pip install tep
```

or domestic mirror:

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

# Docs

[fixture_env_vars, a global variable](https://github.com/dongfanger/tep/blob/master/docs/fixture_env_vars%2C%20a%20global%20variable.md)

[fixture_login, reuse a api](https://github.com/dongfanger/tep/blob/master/docs/fixture_login%2C%20reuse%20a%20api.md)

# More Usage

If you want to know more usages, you can read [pytest docs](https://docs.pytest.org/).

You know pytest.

You know tep.

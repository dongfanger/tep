Create file fixtures/fixture_env_vars.py: 

```python
#!/usr/bin/python
# encoding=utf-8

from tep.dao import mysql_engine
from tep.fixture import *


@pytest.fixture(scope="session")
def env_vars(config):
    class Clazz(TepVars):
        env = config["env"]

        """Variables define start"""
        # Environment and variables
        mapping = {
            "qa": {
                "domain": "https://qa.com",
                "mysql_engine": mysql_engine("127.0.0.1",  # host
                                             "2306",  # port
                                             "root",  # username
                                             "123456",  # password
                                             "qa"),  # db_name
            },
            "release": {
                "domain": "https://release.com",
                "mysql_engine": mysql_engine("127.0.0.1",
                                             "2306",
                                             "root",
                                             "123456",
                                             "release"),
            }
            # Add your environment and variables
        }
        # Define properties for auto display
        domain = mapping[env]["domain"]
        mysql_engine = mapping[env]["mysql_engine"]
        """Variables define end"""

    return Clazz()

```

Using in the tests/test.py:

```python
def test(env_vars):
    url = env_vars.domain + "\api"
```

or:

```python
# test_put.py
def test_put(env_vars):
    env_vars.put("name", "dongfanger")

# test_get.py
def test_get(env_vars):
    env_vars.get("name")
```


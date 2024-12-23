import json

import pytest
from filelock import FileLock
from tep import request


@pytest.fixture(scope="session")
def login_xdist(tmp_path_factory, worker_id):
    """
    Xdist is used in a distributed manner, and this login will only be executed globally once throughout the entire runtime
    Reference: https://pytest-xdist.readthedocs.io/en/latest/how-to.html#making-session-scoped-fixtures-execute-only-once
    """

    def _login():
        url = "http://127.0.0.1:5000/login"
        headers = {"Content-Type": "application/json"}
        body = {"username": "dongfanger", "password": "123456"}
        response = request("post", url=url, headers=headers, json=body)
        assert response.status_code < 400
        return {"Content-Type": "application/json", "Cookie": f"{response.json()['Cookie']}"}

    if worker_id == "master":
        # not executing in with multiple workers, just produce the data and let
        # pytest's fixture caching do its job
        return _login

    # get the temp directory shared by all workers
    root_tmp_dir = tmp_path_factory.getbasetemp().parent

    fn = root_tmp_dir / "data.json"
    with FileLock(str(fn) + ".lock"):
        if fn.is_file():
            _function = json.loads(fn.read_text())
        else:
            _function = _login
            fn.write_text(json.dumps(_function))
    return _function

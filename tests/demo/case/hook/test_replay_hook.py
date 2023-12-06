import os

from loguru import logger

from tep.libraries.Config import Config
from tep.libraries.Har import Har


def test():
    profile = {
        "harFile": os.path.join(Config.BASE_DIR, "data", "har", "flow.har"),
        "overwrite": True,
        "hookVar": {"domain": "http://127.0.0.1:5000"},
        "hookUrl": {"http://127.0.0.1:5000": "${domain}"},
        "hookHeaders": {"Content-Type": "application/json", "Cookie": "de2e3ffu29"}
    }
    Har(profile).har2case()

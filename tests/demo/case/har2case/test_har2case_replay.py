import os

from loguru import logger

from tep.libraries.Config import Config
from tep.libraries.Har import Har


def test():
    profile = {
        "harFile": os.path.join(Config.BASE_DIR, "case", "har", "demo.har"),
        "replay": True,
        "overwrite": True
    }
    Har(profile).har2case()

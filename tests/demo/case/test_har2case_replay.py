import os

from loguru import logger

from tep.libraries.Config import Config
from tep.libraries.Har import Har


def test():
    har_file = os.path.join(Config.BASE_DIR, "case", "har", "demo.har")
    profile = {"replay": True}
    Har(har_file, profile).har2case()

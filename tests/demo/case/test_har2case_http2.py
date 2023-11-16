import os

from tep.libraries.Config import Config
from tep.libraries.Har import Har


def test():
    har_file = os.path.join(Config.BASE_DIR, "data", "demo.har")
    profile = {"http2": True}
    Har(har_file, profile).har2case()

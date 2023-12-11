import os

from tep.libraries.Config import Config
from tep.libraries.Har import Har


def test():
    profile = {
        "harFile": os.path.join(Config.BASE_DIR, "case", "har", "demo.har"),
        "http2": True
    }
    Har(profile).har2case()

import os

from tep.libraries.Config import Config
from tep.libraries.Har import Har


def test():
    profile = {
        "harFile": os.path.join(Config.BASE_DIR, "data", "har", "demo.har"),
        "overwrite": True,
        "jsonIndent": 4
    }
    Har(profile).har2case()

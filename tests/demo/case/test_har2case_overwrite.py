import os

from tep.libraries.Config import Config
from tep.libraries.Har import Har


def test():
    profile = {
        "harDir": os.path.join(Config.BASE_DIR, "data", "har"),
        "desDir": os.path.join(Config.BASE_DIR, "case", "replay"),
        "overwrite": True
    }
    Har(profile).har2case()

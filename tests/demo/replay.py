import os

from tep.libraries.Config import Config
from tep.libraries.Har import Har

if __name__ == '__main__':
    profile = {
        "harDir": os.path.join(Config.BASE_DIR, "data", "har"),
        "desDir": os.path.join(Config.BASE_DIR, "case", "replay")
    }
    Har(profile).har2case()

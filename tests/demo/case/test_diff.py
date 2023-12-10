import os

from tep.libraries.Config import Config
from tep.libraries.Diff import Diff


def test():
    Diff.make("023f387db398504889e0afb8dd1bc99d", os.path.join(Config.BASE_DIR, "case", "har", "demo-replay-diff"))

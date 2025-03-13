import os

from tep import har2case
from tep.config import Config


def test():
    har2case({
        'har': os.path.join(Config().FILE_DIR, 'har', 'flow.har'),
        'dir': os.path.join(Config().TESTS_DIR, 'generated'),
        'overwrite': 1,
        'var': {'domain': 'http://127.0.0.1:5000'},
        'url': {'http://127.0.0.1:5000': '${domain}'},
        'headers': {'Content-Type': 'application/json', 'Cookie': 'de2e3ffu29'}
    })

import os

from haralyzer import HarParser

from tep.libraries.Config import Config


def test():
    har_parser = HarParser.from_file(os.path.join(Config.BASE_DIR, "data", "demo.har"))
    for page in har_parser.pages:
        for entry in page.entries:
            print(entry.request.url)
            print(entry.request.method)
            print(entry.request.headers)
            print(entry.request.cookies)
            print(entry.request.text)
            print(entry.response.text)

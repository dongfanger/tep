import base64
import os

from haralyzer import HarParser

from tep.libraries.Config import Config


def test():
    har_parser = HarParser.from_file(os.path.join(Config.BASE_DIR, "case", "har", "demo.har"))
    for page in har_parser.pages:
        for entry in page.entries:
            print(entry.request.url)
            print(entry.request.method)
            print(entry.request.headers)
            print(entry.request.cookies)

            text = entry.response.text
            if text:
                mime_type = entry.response.mimeType
                if mime_type and mime_type.startswith("application/json"):
                    encoding = entry.response.textEncoding
                    if encoding and encoding == "base64":
                        content = base64.b64decode(text).decode('utf-8')
                        print(content)

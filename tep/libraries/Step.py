from tep.libraries.Request import Request


class Before:
    def __init__(self):
        self.parametrize: list = []


class After:
    def __init__(self):
        self.extractor: list = []
        self.assertion: list = []
        self.replay: list = []


class Step:
    def __init__(self):
        self.name: str = ""
        self.before: Before = Before()
        self.request: Request = Request()
        self.after: After = After()

class Profile:
    def __init__(self):
        self.har_file: str = ""
        self.har_dir: str = ""
        self.des_dir: str = ""
        self.overwrite: bool = False
        self.replay: bool = False
        self.json_indent: int = 4
        self.http2: bool = False
        self.hook_var: dict = {}
        self.hook_url: dict = {}
        self.hook_headers: dict = {}

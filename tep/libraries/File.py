#!/usr/bin/python
# encoding=utf-8

import json
import os

import yaml


class File:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> [dict, list]:
        file_type = self._file_type()
        if file_type in [".yml", ".yaml", ".YML", "YAML"]:
            return self._yaml_load()
        if file_type in [".json", ".JSON"]:
            return self._json_load()

    def _file_type(self) -> str:
        return os.path.splitext(self.path)[-1]

    def _yaml_load(self) -> [dict, list]:
        with open(self.path, encoding="utf8") as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)

    def _json_load(self) -> [dict, list]:
        with open(self.path, encoding="utf8") as f:
            return json.load(f)

#!/usr/bin/python
# encoding=utf-8
import json


def simplify_json(json_str: str) -> str:
    data = json.loads(json_str)
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)


def beautify_json(json_str: str, indent: int = 4) -> str:
    data = json.loads(json_str)
    return json.dumps(data, separators=(',', ':'), indent=indent, ensure_ascii=False)


def parse(json_str: str) -> dict:
    return json.loads(json_str)


def to_json_str(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False)

#!/usr/bin/python
# encoding=utf-8
import os


class Constant:
    VERSION = "3.0.4"


def set_version():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    toml_path = os.path.join(base_path, "pyproject.toml")
    cli_path = os.path.join(base_path, "tep", "cli.py")

    replace(toml_path, "version = ")  # pyproject.toml
    replace(cli_path, "    version = ")  # cli.py


def replace(path, prefix):
    with open(path, encoding="utf8") as fr:
        content = fr.read().splitlines()
        new = ""
        for line in content:
            if line.startswith(prefix):
                line = prefix + f'"{Constant.VERSION}"'

            new += line + "\n"
        with open(path, "w", encoding="utf8") as fw:
            fw.write(new)


if __name__ == '__main__':
    set_version()

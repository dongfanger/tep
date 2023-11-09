#!/usr/bin/python
# encoding=utf-8

import argparse
import sys

from tep import __description__, __version__
from tep.scaffold import scaffold


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-v", "--version", dest="version", action="store_true", help="show version")
    parser.add_argument("-s", "--startproject", metavar='project_name', type=str, help="Create a new project with template structure")
    parser.add_argument("-venv", dest="create_venv", action="store_true", help="Create virtual environment in the project, and install tep")

    if len(sys.argv) == 1:
        # tep
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        if sys.argv[1] in ["-v", "--version"]:
            print(f"Current Version: V{__version__}")
            print(r"""
 ____o__ __o____   o__ __o__/_   o__ __o
  /   \   /   \   <|    v       <|     v\
       \o/        < >           / \     <\
        |          |            \o/     o/
       < >         o__/_         |__  _<|/
        |          |             |
        o         <o>           <o>
       <|          |             |
       / \        / \  _\o__/_  / \
""")
        elif sys.argv[1] in ["-h", "--help"]:
            parser.print_help()
        elif sys.argv[1] in ["-s", "--startproject"]:
            parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if sys.argv[1] in ["-s", "--startproject"]:
        scaffold(args)

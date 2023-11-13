#!/usr/bin/python
# encoding=utf-8

import argparse
import sys

from tep import __description__, __version__
from tep.scaffold import init_parser_scaffold, scaffold


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-V", "--version", dest="version", action="store_true", help="show version")
    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_scaffold = init_parser_scaffold(subparsers)

    if len(sys.argv) == 1:
        # tep
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        if sys.argv[1] in ["-V", "--version"]:
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
        elif sys.argv[1] == "new":
            sub_parser_scaffold.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if sys.argv[1] == "new":
        scaffold(args)

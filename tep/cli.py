#!/usr/bin/python
# encoding=utf-8

import argparse
import sys

from tep.scaffold import scaffold, init_parser_scaffold


def main():
    version = "3.0.6"
    parser = argparse.ArgumentParser(description='Try Easy Pytest!')
    parser.add_argument('-V', '--version', dest='version', action='store_true', help='show version')
    subparsers = parser.add_subparsers(help='sub-command help')
    sub_parser_scaffold = init_parser_scaffold(subparsers)

    if len(sys.argv) == 1:
        # tep
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['-V', '--version']:
            print(f'Current Version: V{version}')
            print(r'Try Easy Pytest!')
            print(r'''
████████ ███████ ██████  
   ██    ██      ██   ██ 
   ██    █████   ██████  
   ██    ██      ██      
   ██    ███████ ██      
''')
        elif sys.argv[1] in ['-h', '--help']:
            parser.print_help()
        elif sys.argv[1] == 'new':
            sub_parser_scaffold.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if sys.argv[1] == 'new':
        scaffold(args)

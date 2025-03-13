#!/usr/bin/python
# encoding=utf-8


def strip(s: str) -> str:
    s = s.strip()
    s = s.strip('\n')
    s = s.strip('\t')
    return s

#!/usr/bin/python
# encoding=utf-8
from tep import v


def test_random():
    s = '''{
    "x": ${random()}
}'''
    print(v(s))


def test_random_n():
    s = '''{
        "x": ${random(9)}
    }'''
    print(v(s))


def test_random_prefix():
    s = '''{
        "x": "${random(前缀,2)}"
    }'''
    print(v(s))


def test_uuid():
    s = '''{
         "x": "${uuid()}"
     }'''
    print(v(s))


def test_time():
    s = '''{
             "x": "${time()}",
         }'''
    print(v(s))


def test_time_format():
    s = '''{
             "x": "${time(%Y-%m-%d %H:%M:%S)}",
         }'''
    print(v(s))


def test_timestamp():
    s = '''{
             "x": "${timestamp()}",
         }'''
    print(v(s))


def test_timestamp_specified():
    s = '''{
             "x": "${timestamp(2023-03-23 23:23:23)}",
         }'''
    print(v(s))

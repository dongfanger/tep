#!/usr/bin/python
# encoding=utf-8


def test():
    from allpairspy import AllPairs

    parameters = [
        ["Brand X", "Brand Y"],
        ["98", "NT", "2000", "XP"],
        ["Internal", "Modem"],
        ["Salaried", "Hourly", "Part-Time", "Contr."],
        [6, 10, 15, 30, 60],
    ]

    for pairs in AllPairs(parameters):
        print(pairs)

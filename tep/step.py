#!/usr/bin/python
# encoding=utf-8
import logging


def step(name: str, function):
    logging.info("----------------" + name + "----------------")
    return function()

#!/usr/bin/python
# encoding=utf-8


import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

from tep.config import Config


class LoggerUtils:
    _logger = None

    @classmethod
    def get_logger(cls, name=None, log_dir=None):
        if cls._logger is None:
            cls._logger = cls._init_logger(name, log_dir)
        return cls._logger

    @classmethod
    def _init_logger(cls, name, log_dir):
        is_tep_tests_run = False

        if name is None:
            name = 'tep'
        if log_dir is None:
            _dir = Config().get_project_dir()
            if _dir:
                is_tep_tests_run = True
                log_dir = os.path.join(Config().get_project_dir(), 'log')
                os.makedirs(log_dir, exist_ok=True)

        _logger = logging.getLogger(name)
        _logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        if is_tep_tests_run:
            current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            log_file = os.path.join(log_dir, f'{current_time}.log')
            file_handler = TimedRotatingFileHandler(
                log_file,
                when='midnight',
                backupCount=7,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            _logger.addHandler(file_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)
            _logger.addHandler(console_handler)

        return _logger


logger = LoggerUtils.get_logger()

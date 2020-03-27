# -*- coding: utf-8 -*-

"""
    有待完善 log日志
"""

import logging


def get_logger(name='Log'):
    value = '%(asctime)s - %(process)d - %(thread)d - %(levelname)s - %(module)s - %(funcName)s: %(lineno)d - %(message)s'
    logging.basicConfig(level=logging.INFO, filemode='log.txt', format=value)
    log = logging.getLogger(name)
    name = name + '.log'
    file_log = logging.FileHandler(name, encoding='utf-8')
    file_log.setLevel(logging.WARNING)
    file_log.setFormatter(logging.Formatter(value))
    log.addHandler(file_log)
    return log



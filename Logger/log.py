# -*- coding: utf-8 -*-

"""
    有待完善 log日志
"""

import logging
import os
from logging import handlers


def get_logger(name='Logger'):
    value = "%(asctime)s - %(process)d - %(thread)d - %(levelname)s - %(module)s - %(funcName)s: %(lineno)d - %(message)s"
    logging.basicConfig(level=logging.INFO, format=value, filemode='Logger.txt')
    logger = logging.getLogger(name)
    log = logging.handlers.TimedRotatingFileHandler(filename='Logger.log', encoding='utf-8', when='D')
    # log = logging.FileHandler('Logger.log', encoding='utf-8')
    log.setLevel(logging.WARNING)
    log.setFormatter(logging.Formatter(value))
    logger.addHandler(log)

    return logger


def get_folder():
    path = os.path.abspath('..')
    path.replace('\\', '/')
    path = path + '/data_file'
    if not os.path.exists(path):
        os.mkdir(path)
    return path

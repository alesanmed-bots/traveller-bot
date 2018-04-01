# encoding: utf-8
"""
logger

Created by Donzok on 19/06/2017.
Copyright (c) 2017 . All rights reserved.
"""

# -*- coding: utf-8 -*-
import logging
import os
import configparser
import sys
import traceback


def init_logger(log_name, log_level=logging.DEBUG):
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("files/elviajante.log")
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    sys.excepthook = log_uncaught_exceptions

def log_uncaught_exceptions(exctype, value, tb):
    config = configparser.ConfigParser()

    config.read(os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../config.ini')
    ))

    logger = logging.getLogger(config['LOGGING']['logger_name'])

    logger.error('{0}\n{1}'.format(value, ''.join(traceback.format_tb(tb))))

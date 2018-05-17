# -*- coding: UTF-8 -*-
import logging
from logging.handlers import RotatingFileHandler
import os

# 新建日志目录
import config

if not os.path.exists(config.LOG_DIR):
    os.makedirs(config.LOG_DIR)


def __get_logger(logger_name):
    level = logging._nameToLevel[config.LOG_LEVEL.upper()]
    file = os.path.join(config.LOG_DIR, logger_name + '.log')
    formatter = logging.Formatter(config.LOG_FORMAT)
    handler = RotatingFileHandler(file, maxBytes=config.MAX_BYTES,
                                  backupCount=config.BACKUP_COUNT,
                                  encoding='UTF-8')
    handler.setFormatter(formatter)
    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


seg_api_logger = __get_logger('seg_api')

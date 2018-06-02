import logging
from logging.handlers import RotatingFileHandler

def logger_factory(logger_name):
    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)
    file_handler = RotatingFileHandler("{}.log".format(logger_name), maxBytes=1024 * 1024 * 100, backupCount=5)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    return log

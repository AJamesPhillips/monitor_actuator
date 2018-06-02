#!/usr/bin/python3

"""
Log network stats to a file
And up to a server
"""

import os
import sys
pwd = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, pwd + "/..") # allows us to import from src/utils etc

from log_stats.log_network_stats import log_network_stats
from utils.logger_factory import logger_factory
from utils.retry import retry_main

log = logger_factory('log_stats')

def main():

    log.info("log stats started")
    log_network_stats(log)


if __name__ == "__main__":

    retry_main(main_function=main, log=log, sleep_on_error_for=100)

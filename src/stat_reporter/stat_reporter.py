#!/usr/bin/python3

"""
Log temperature to a file
And up to a server

Based off http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/ example
"""

import os
import sys
pwd = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, pwd + "/..") # allows us to import from src/utils etc
import subprocess
import re

from utils.get_config import get_config
from utils.logger_factory import logger_factory
from utils.retry import retry_main
from utils.batch_send_factory import batch_send_factory
from utils.intervaled_ma import intervaled_ma


log = logger_factory('stat_reporter')


def log_network_stats(log, config, now):
    try:
        process = subprocess.Popen(
            args=["netstat", "-s"],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        """
            48692 segments received
            23618
            124 segments retransmited
            0 bad segments received.
        """
        text = process.communicate()[0].decode("utf-8")

        to_match = [
            "segments received",
            "segments send out",
            "segments retransmited",
            "bad segments received"
        ]

        metrics = dict()
        batched = []
        node_name = config["node_name"]

        for metric_string in to_match:
            metric_match = re.match('.*(\d+) {}.*'.format(metric_string), text, re.DOTALL)
            metric = int(metric_match.group(1))
            metrics[metric_string] = metric
            metric_type = "stats-{}".format(metric_string.replace(' ', '_'))
            data = {
                "type": metric_type,
                "datetime": now,
                "tags": [node_name + " " + metric_type],
                "value": metric,
            }
            batched.append(data)

        metric_type = "stats-ratio_retransmitted_packets"
        value = metrics["segments retransmited"] / metrics["segments send out"] if metrics["segments send out"] > 0 else 0
        data = {
            "type": metric_type,
            "datetime": now,
            "tags": [node_name + " " + metric_type],
            "value": value,
        }
        batched.append(data)
        return batched
    except Exception as e:
        log.exception("Reading from netstat received error: \"{}\"".format(e))
        return []


def action_func_factory(log, config):

    log.info('Got config: {}'.format(config["stat_reporter"]))

    def action_func(now):

        stats = []
        if config["stat_reporter"]["enabled"]:
            stats = stats + log_network_stats(log=log, config=config, now=now)
        return stats

    return action_func


def main():

    log.info("log stats started")
    config = get_config(service_name='stat_reporter', log=log)
    action_func = action_func_factory(log=log, config=config)
    batch_func = batch_send_factory(log=log, config=config, verify_ssl_certificate=False)
    intervaled_ma(
        log=log,
        action_func=action_func,
        batch_func=batch_func,
        batch_limit=1,
        min_seconds_between_actions=100
    )


if __name__ == "__main__":

    retry_main(main_function=main, log=log)

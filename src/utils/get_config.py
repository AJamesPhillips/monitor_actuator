import json5
import socket
import os
pwd = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
import sys


def get_config(service_name, log):
    with open(pwd + "/../../private/{}/config.json5".format(service_name), "r") as f:
        all_config = json5.loads(f.read())
    current_host = socket.gethostname()

    nodes = list(filter(lambda node: node["node_name"] == current_host, all_config["nodes"]))

    if len(nodes) != 1:
        host_names = list(map(lambda node: node["node_name"], all_config["nodes"]))
        log.error("unsupported node hostname \"{}\" in hostnames \"{}\"".format(current_host, host_names))
        sys.exit(1)


    return nodes[0]

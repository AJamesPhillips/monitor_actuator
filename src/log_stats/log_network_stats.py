#!/usr/bin/python3

"""
Log network stats to a file
And up to a server
"""

import os
import sys
pwd = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, pwd + "/..") # allows us to import from src/utils etc

from utils.json_helper import safe_json

# def get_config():
#     with open(pwd + "/../../private/temperature_sensor/config.json5", "r") as f:
#         all_config = json5.loads(f.read())
#     current_host = socket.gethostname()

#     nodes = list(filter(lambda node: node["node_name"] == current_host, all_config["nodes"]))

#     if len(nodes) != 1:
#         host_names = list(map(lambda node: node["node_name"], all_config["nodes"]))
#         log("EXCEPTION: unsupported node hostname \"{}\" in hostnames \"{}\"".format(current_host, host_names))
#         sys.exit(1)

#     return nodes[0]


# def get_temp_from_device(device_uid):
#     try:
#         with open("/sys/bus/w1/devices/{}/w1_slave".format(device_uid)) as tfile:
#             text = tfile.read()
#     except Exception as e:
#         log("error: Reading from device \"{}\", received error: \"{}\"".format(device_uid, e))
#         return None

#     secondline = text.split("\n")[1]
#     temperaturedata = secondline.split(" ")[9]
#     # The first two characters are "t=", so get rid of those and convert the
#     # temperature from a string to a number.
#     temperature_milliCelcius = float(temperaturedata[2:])
#     temperature_celcius = temperature_milliCelcius / 1000
#     return temperature_celcius

# from time import sleep

def log_network_stats(log):

    log.info("log network stats started")
    sleep(5)
    # config = get_config()

    # batched = []
    # batch_limit = 10
    # max_sample_frequency_seconds = 10
    # last_sample_datatime = None

    # while True:
    #     # read from device(s) and write to the log file
    #     now = datetime.datetime.now()

    #     if last_sample_datatime:
    #         diff = max((now - last_sample_datatime).total_seconds(), 0)
    #         if diff < max_sample_frequency_seconds:
    #             sleep_for = max_sample_frequency_seconds - diff
    #             log("info: time elapsed: {}, sleeping for {}".format(diff, sleep_for))
    #             sleep(sleep_for)

    #     for thermometer in config["thermometers"]:

    #         device_uid = thermometer["device_uid"]
    #         device_tags = thermometer["tags"]

    #         temperature_celcius = get_temp_from_device(device_uid=device_uid)
    #         log("data: {}, {}, {}, {}".format(now, device_uid, device_tags, temperature_celcius))
    #         batched.append({
    #             "type": "thermometer",
    #             "datetime": now,
    #             "device_uid": device_uid,
    #             "tags": device_tags,
    #             "value": temperature_celcius,
    #         })

    #     if len(batched) >= batch_limit:
    #         log("info: sending batch of data containing {} entries".format(len(batched)))
    #         try:
    #             # TODO better error handling needed if / when multiple endpoint subscribers
    #             for endpoint in config["endpoints"]:
    #                 data = safe_json({"data": batched})
    #                 log("info: Posting data: \"{}\"".format(data))
    #                 credentials = endpoint["credentials"]
    #                 requests.post(endpoint["endpoint_url"],
    #                     data=data,
    #                     auth=(credentials["username"], credentials["password"]),
    #                     timeout=1, # 1 second
    #                 )
    #             batched = []
    #         except Exception as e:
    #             log("error: Posting data to endpoint, received error \"{}\"".format(e))

    #     last_sample_datatime = now

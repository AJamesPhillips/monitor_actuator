#!/usr/bin/python3

"""
Log temperature to a file

Based off http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/ example
"""

import os
import sys
pwd = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(1, pwd + "/../..")
from time import sleep
import datetime
import json5
import socket
import traceback

import requests


def get_config():
    with open(pwd + "/../../private/temperature_sensor/config.json5", "r") as f:
        all_config = json5.loads(f.read())
    current_host = socket.gethostname()

    nodes = list(filter(lambda node: node["node_name"] == current_host, all_config["nodes"]))

    if len(nodes) != 1:
        host_names = list(map(lambda node: node["node_name"], all_config["nodes"]))
        write_to_file("EXCEPTION: unsupported node hostname \"{}\" in hostnames \"{}\"".format(current_host, host_names))
        sys.exit(1)

    return nodes[0]


def write_to_file(text_to_write, extra = "\n"):
    with open("temperature.log", "a") as f:
        f.write(text_to_write + extra)
    # print(text_to_write)


def get_temp_from_device(device_uid):
    try:
        with open("/sys/bus/w1/devices/{}/w1_slave".format(device_uid)) as tfile:
            text = tfile.read()
    except Exception as e:
        write_to_file("error: Reading from device \"{}\", received error: \"{}\"".format(device_uid, e))
        return None

    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    # The first two characters are "t=", so get rid of those and convert the
    # temperature from a string to a number.
    temperature_milliCelcius = float(temperaturedata[2:])
    temperature_celcius = temperature_milliCelcius / 1000
    return temperature_celcius


def main():

    config = get_config()

    write_to_file("header: datetime, device_uuid, device_name, temperature_celcius")

    batched = []
    batch_limit = 10
    max_sample_frequency_seconds = 10
    last_sample_datatime = None

    while True:
        # read from device(s) and write to the log file
        now = datetime.datetime.now()

        if last_sample_datatime:
            diff = (now - last_sample_datatime).total_seconds()
            if diff < max_sample_frequency_seconds:
                sleep_for = max_sample_frequency_seconds - diff
                write_to_file("info: sleeping for {}".format(sleep_for))
                sleep(sleep_for)

        for thermometer in config["thermometers"]:

            device_uid = thermometer["device_uid"]
            device_name = thermometer["name"]

            temperature_celcius = get_temp_from_device(device_uid=device_uid)
            write_to_file("data: {}, {}, {}, {}".format(now, device_uid, device_name, temperature_celcius))
            batched.append({
                "type": "thermometer",
                "datetime": now,
                "device_uid": device_uid,
                "name": device_name,
                "value": temperature_celcius,
            })

        if len(batched) >= batch_limit:
            write_to_file("info: sending batch of data containing {} entries".format(len(batched)))
            try:
                # TODO better error handling needed if / when multiple endpoint subscribers
                for endpoint in config["endpoints"]:
                    data = {"data": batched}
                    write_to_file("info: Posting data: \"{}\"".format(data))
                    credentials = endpoint["credentials"]
                    requests.post(endpoint["endpoint_url"], data=data, auth=(credentials["username"], credentials["password"]))
            except Exception as e:
                write_to_file("error: Posting data to endpoint, received error \"{}\"".format(e))

            batched = []

        last_sample_datatime = now


def retry_main():

    sleep_for = 10
    max_sleep_for = 10 * 16

    while True:
        try:
            main()
        except Exception as e:
            write_to_file("error: main received error, sleep for {}, error received: \"{}\"".format(sleep_for, e))
            write_to_file("error: traceback.format_exc(): \"{}\"".format(traceback.format_exc()))
            sleep(sleep_for)
            sleep_for = min(sleep_for * 2, max_sleep_for)


if __name__ == "__main__":

    retry_main()

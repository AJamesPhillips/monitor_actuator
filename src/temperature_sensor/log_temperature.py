#!/usr/bin/python3

"""
Log temperature to a file

Based off http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/ example
"""

import os
import sys
sys.path.insert(1, os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..'))

import datetime
import time


THERMOMETER_UIDS = (
    '28-0000074ac18d',
    '28-0000074b20c0',
    '28-0000074b4e44',
)


def write_to_file(text_to_write):
    f = open('temperature_log.csv', 'a')
    f.write(text_to_write)
    f.closed


def get_temp_from_device(device_uid):
    with open("/sys/bus/w1/devices/{}/w1_slave".format(device_uid)) as tfile:
        text = tfile.read()

    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    # The first two characters are "t=", so get rid of those and convert the
    # temperature from a string to a number.
    temperature_milliCelcius = float(temperaturedata[2:])
    temperature_celcius = temperature_milliCelcius / 1000
    return temperature_celcius


def main():
    import plotly.plotly as plty
    from private.src.credentials_plotly import (
        plotly_streaming_token,
        plotly_api_key,
        plotly_username,
    )

    write_to_file("datetime, device_uuid, temperature_celcius\n")

    # Set up plotly stream
    plty.sign_in(plotly_username, plotly_api_key)
    stream = plty.Stream(plotly_streaming_token)
    stream.open()

    while True:
        # read from device(s) and write to the log file
        now = datetime.datetime.now()
        temps_by_device_uid = {}
        for device_uid in THERMOMETER_UIDS:
            temperature_celcius = get_temp_from_device(device_uid=device_uid)
            write_to_file("{}, {}, {}\n".format(now, device_uid, temperature_celcius))
            temps_by_device_uid[device_uid] = temperature_celcius

        for (device_uid, temperature_celcius) in temps_by_device_uid.items():
            stream.write({'x': now, 'y': temperature_celcius})

        # wait before reading again
        # Note: Plotly will close stream after 60 seconds of inactivity
        # https://plot.ly/streaming/  "If a minute passes without receiving any
        # data from the client the stream connection will be closed" so put in a
        # heartbeat call
        time.sleep(30)
        stream.heartbeat()
        time.sleep(30)

main()

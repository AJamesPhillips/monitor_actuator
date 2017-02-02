#!/usr/bin/python3

"""
Log temperature to a file

Based off ADCPi/demo-logvoltage.py example from
https://github.com/abelectronicsuk/ABElectronics_Python3_Libraries
"""

import os
import sys
sys.path.insert(1, os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..'))

from lib.ABElectronics_Python3_Libraries.ADCPi.ABE_ADCPi import ADCPi
from lib.ABElectronics_Python3_Libraries.ADCPi.ABE_helpers import ABEHelpers
import datetime
import time

from .voltage_temperature_converter import (
    convert_therm01_in_adc__2017_01_31__voltage_to_temp as convert01_v_to_temp
)


def write_to_file(text_to_write):
    f = open('temperature_log.csv', 'a')
    f.write(text_to_write)
    f.closed


def main():
    import plotly.plotly as plty
    from private.src.credentials_plotly import (
        plotly_streaming_token,
        plotly_api_key,
        plotly_username,
    )

    i2c_helper = ABEHelpers()
    bus = i2c_helper.get_smbus()
    sample_resolution = 18  # Is sampling bits not rate, and can be 12, 14, 16, 18
    adc = ADCPi(bus, 0x68, 0x69, sample_resolution)

    write_to_file("datetime, channel1_voltage, channel1_temperature\n")

    # Set up plotly stream
    plty.sign_in(plotly_username, plotly_api_key)
    stream = plty.Stream(plotly_streaming_token)
    stream.open()

    while True:
        # read from adc channel(s) and write to the log file
        channel1_voltage = adc.read_voltage(1)
        channel1_temperature = convert01_v_to_temp(channel1_voltage)
        now = datetime.datetime.now()
        write_to_file("{}, {}, {}\n".format(now, channel1_voltage, channel1_temperature))

        stream.write({'x': now, 'y': channel1_temperature})

        # wait before reading again
        # Note: Plotly will close stream after 60 seconds of inactivity
        # https://plot.ly/streaming/  "If a minute passes without receiving any
        # data from the client the stream connection will be closed"
        time.sleep(30)
        stream.write('')
        time.sleep(30)

main()

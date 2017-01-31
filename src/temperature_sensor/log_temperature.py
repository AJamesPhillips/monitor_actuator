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
    i2c_helper = ABEHelpers()
    bus = i2c_helper.get_smbus()
    adc = ADCPi(bus, 0x68, 0x69, 12)

    write_to_file("datetime, channel1_voltage, channel1_temperature")

    while True:
        # read from adc channel(s) and write to the log file
        channel1_voltage = adc.read_voltage(1)
        channel1_temperature = convert01_v_to_temp(channel1_voltage)
        write_to_file("{}, {}, {}\n".format(datetime.datetime.now(), channel1_voltage, channel1_temperature))

        # wait before reading again
        time.sleep(60)


main()

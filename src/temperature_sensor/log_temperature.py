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

from characterise_thermistor import C_TO_KELVIN, resistance_to_temperature_kelvin


def write_to_file(text_to_write):
    f = open('temperature_log.csv', 'a')
    f.write(text_to_write)
    f.closed


def make_voltage_to_temperature_converter(constant_resistance, a, b, c):
    # From characterise_thermistor.py
    def converter(voltage_accross_thermistor):
        # Using the voltage divider equation:
        #    voltage_accross_thermistor = thermistor_resistance / (thermistor_resistance + constant_resistance)
        #    (thermistor_resistance + constant_resistance) * voltage_accross_thermistor = thermistor_resistance
        #    (thermistor_resistance * voltage_accross_thermistor) + (constant_resistance * voltage_accross_thermistor) = thermistor_resistance
        #    constant_resistance * voltage_accross_thermistor = thermistor_resistance - (thermistor_resistance * voltage_accross_thermistor)
        #    constant_resistance * voltage_accross_thermistor = thermistor_resistance * (1 - voltage_accross_thermistor)
        #    (constant_resistance * voltage_accross_thermistor) / (1 - voltage_accross_thermistor) = thermistor_resistance
        thermistor_resistance = (constant_resistance * voltage_accross_thermistor) / (1 - voltage_accross_thermistor)

        # Steinhart-Hart_equation
        return resistance_to_temperature_kelvin(thermistor_resistance, a, b, c) - C_TO_KELVIN
    return converter


def main():
    i2c_helper = ABEHelpers()
    bus = i2c_helper.get_smbus()
    adc = ADCPi(bus, 0x68, 0x69, 12)

    write_to_file("datetime, channel1_voltage, channel1_temperature")
    channel1_parameters = {
        'constant_resistance': 4700,
        # From characterise_thermistor.py using Steinhart-Hart_equation
        'a': -2161.21683309,
        'b': 472.21473306,
        'c': -2.43223168,
    }
    convert_channel1_voltage_to_temp = make_voltage_to_temperature_converter(**channel1_parameters)
    while True:
        # read from adc channel(s) and write to the log file
        channel1_voltage = adc.read_voltage(1)
        channel1_temperature = convert_channel1_voltage_to_temp(channel1_voltage)
        write_to_file("{}, {}, {}\n".format(datetime.datetime.now(), channel1_voltage, channel1_temperature))

        # wait 1 second before reading the pins again
        time.sleep(60)


main()

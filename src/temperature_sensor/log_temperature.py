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

from utils.get_config import get_config
from utils.logger_factory import logger_factory
from utils.retry import retry_main
from utils.batch_send_factory import batch_send_factory
from utils.intervaled_ma import intervaled_ma


log = logger_factory('log_temperature')


def get_temp_from_device(device_uid):
    try:
        with open("/sys/bus/w1/devices/{}/w1_slave".format(device_uid)) as tfile:
            text = tfile.read()
    except Exception as e:
        log.exception("Reading from device \"{}\", received error: \"{}\"".format(device_uid, e))
        return None

    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    # The first two characters are "t=", so get rid of those and convert the
    # temperature from a string to a number.
    temperature_milliCelcius = float(temperaturedata[2:])
    temperature_celcius = temperature_milliCelcius / 1000
    return temperature_celcius


def action_func_factory(log, config):

    log.info('Got thermometers: {}'.format(config["thermometers"]))

    def action_func(now):

        batched = []
        for thermometer in config["thermometers"]:

            device_uid = thermometer["device_uid"]
            device_tags = thermometer["tags"]

            temperature_celcius = get_temp_from_device(device_uid=device_uid)
            data = {
                "type": "thermometer",
                "datetime": now,
                "device_uid": device_uid,
                "tags": device_tags,
                "value": temperature_celcius,
            }
            log.info("data: \"{}\"".format(data))
            batched.append(data)

        return batched

    return action_func


def main():

    config = get_config(service_name='temperature_sensor', log=log)
    log.info("header: datetime, device_uuid, device_tags, temperature_celcius")
    action_func = action_func_factory(log=log, config=config)
    batch_func = batch_send_factory(log=log, config=config)
    intervaled_ma(
        log=log,
        action_func=action_func,
        batch_func=batch_func,
        batch_limit=10,
        min_seconds_between_actions=10
    )


if __name__ == "__main__":

    retry_main(main_function=main, log=log)

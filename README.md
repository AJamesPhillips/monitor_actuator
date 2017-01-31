
# Multi node

A repo to contain code for setting up and running a system(s) for aiding in
monitoring and actuating.

Example use cases include:

* temperature monitor(s) for warning fridge/freezer failure
* webcam(s) for taking periodic photos of the lab as extra aides to protecting
  the occupants and the space, as well as potential usage stats to inform
  debate.
* sense RFID
* enabled / disable equipment


## Deploying

Private values live in the `multi_node/private` directory and include things
such as your inventory file and private group_vars.

### Activate Ansible

    $ source deploy/ansible/hacking/env-setup


## Temperature logger

Built for raspberry pi zero with [ADC board from ABElectronics](https://www.abelectronics.co.uk/p/69/ADC-Pi-Zero-Raspberry-Pi-Analogue-to-Digital-converter)
5V from board Vcc used in voltage divider with 9.4 k ohm and the thermister.
TODO, electrical implementation should use a voltage reference instead of 5V
from the board.

### Deploy logger

    $ ansible-playbook deploy/playbook_temperature_sensor.yml -i deploy/private/inventory

### Start logger

    raspberrypi:~ $ nohup python3 -m multi_node.src.temperature_sensor.log_temperature &


## Tests

    $  PYTHONPATH=`pwd` pytest tests/**/* --pdb


# Monitor Actuator

A repo to contain code for setting up and running a system(s) for aiding in
monitoring and actuating.

Example use cases include:

* temperature monitor(s) for warning fridge/freezer failure
* webcam(s) for taking periodic photos of the lab as extra aides to protecting
  the occupants and the space, as well as potential usage stats to inform
  debate.
* sense RFID
* enabled / disable equipment

## TODO

- [ ] Implement autogeneration of ssh_auto_generated.cfg file
- [x] Is it possible to run provisioning through an ssh tunnel?

### TODO automate provisioning of MA_NODE(s):

- [ ] Use https://github.com/pinkeen/ansible-role-ssh-tunnel-client
- [ ] if not present in /etc/monitor_actuator/MA_NODE_UUID,  set MA_NODE_UUID number to NEXT_MA_NODE_UUID and
- [ ]     increment (by 2) and update NEXT_MA_NODE_UUID in local provision repo
- [ ] add wifi details
- [ ] add script to try (re)connecting to wifi if available
- [ ] add MA_CONTROLPOINT_KEY to authorised_keys
- [ ] MA_NODE_NAME = node{{ MA_NODE_UUID }}
- [ ] generate key and store as MA_NODE_NAME
- [ ] auto retry script + cron to run `ssh -f -N -T -R{{ PORT }}:localhost:22 root@{{ MA_CONTROLPOINT_IP }} -i {{ MA_NODE_NAME }}` every minute
      where PORT is 20000 + MA_NODE_UUID, MA_CONTROLPOINT_IP is for example 123.123.123.123
- [ ] also set up ssh tunnel where PORT = 20000 + MA_NODE_UUID + 1  and  kill and restart this process every minute

### TODO automate provisioning of MA_CONTROLPOINT:

- [ ] Use https://github.com/pinkeen/ansible-role-ssh-tunnel-server
- [ ] adding MA_NODE key(s) to authorised_keys
- [ ] add following to /controlpoint/.ssh/config AND local:

          Host ma_node1
              HostName localhost
              User pi
              IdentityFile /controlpoint/.ssh/key
              Port 22222

### TODO local:

- [ ] update local ~/.ssh/config with (and ma_node entries above + ProxyCommand)

          Host ma_controlpoint
              HostName 123.123.123.123
              User root
              IdentityFile /local/.ssh/key

          Host ma_node1
              HostName localhost
              User pi
              Port 22222
              # Do not need for local, only on controlpoint
              IdentityFile /controlpoint/.ssh/key
              ProxyCommand ssh ma_controlpoint -W %h:%p


### TODO other

- [ ] Add streaming of multiple data to same plotly graph
- [ ] Handle and recover from the following error:

    Traceback (most recent call last):
      File "/usr/lib/python3.4/runpy.py", line 170, in _run_module_as_main
        "__main__", mod_spec)
      File "/usr/lib/python3.4/runpy.py", line 85, in _run_code
        exec(code, run_globals)
      File "/home/pi/multi_node/src/temperature_sensor/log_temperature.py", line 65, in <module>
        main()
      File "/home/pi/multi_node/src/temperature_sensor/log_temperature.py", line 57, in main
        stream.write({'x': now, 'y': channel1_temperature})
      File "/usr/local/lib/python3.4/dist-packages/plotly/plotly/plotly.py", line 656, in write
        self._stream.write(jdata, reconnect_on=reconnect_on)
      File "/usr/local/lib/python3.4/dist-packages/plotly/plotly/chunked_requests/chunked_request.py", line 36, in write
        if not self._isconnected():
      File "/usr/local/lib/python3.4/dist-packages/plotly/plotly/chunked_requests/chunked_request.py", line 289, in _isconnected
        raise e
      File "/usr/local/lib/python3.4/dist-packages/plotly/plotly/chunked_requests/chunked_request.py", line 247, in _isconnected
        self._bytes = self._conn.sock.recv(1)
    ConnectionResetError: [Errno 104] Connection reset by peer


## Deploying

### Private values

Private values live in the `private/` directory include things such as your
inventory file for deployment and credentials for various services.
You will need to edit the `*.template*` files before being able to deploy the
code.  We recommend you run `git init` inside the `private/` directory and
commit private credentials / config to a private repository.

### Activate Ansible

    $ source deploy/ansible/hacking/env-setup


## Temperature logger

### Option 1: ADC

Built for raspberry pi zero with [ADC board from ABElectronics](https://www.abelectronics.co.uk/p/69/ADC-Pi-Zero-Raspberry-Pi-Analogue-to-Digital-converter)
5V from board Vcc used in voltage divider with 9.4 k ohm and the thermister.
TODO, electrical implementation should use a voltage reference instead of 5V
from the board.

### Option 2: Digital DS18B20

1-Wire DS18B20
Buy from ebay, £11 for 5: [5pcs DS18b20 Waterproof Temperature Sensor Thermal Probe Thermometer Durable 2M](http://www.ebay.co.uk/itm/162158276878)
Using these instructions
Wire up RED=Vcc BLACK=GND WHITE/YELLOW=SIG so that Vcc is 5V supply and Sig is GPIO4
Add lines to end of /etc/modules:
w1-gpio
w1-therm




### Deploy logger

    $ ansible-playbook playbook_temperature_sensor.yml -i ../private/deploy/inventory

### Start logger

    raspberrypi:~ $ nohup python3 -m monitor_actuator.src.temperature_sensor.log_temperature &


## Tests

    $  PYTHONPATH=`pwd` pytest tests/**/* --pdb

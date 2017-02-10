
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

Handle and recover from the following error:

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

Built for raspberry pi zero with [ADC board from ABElectronics](https://www.abelectronics.co.uk/p/69/ADC-Pi-Zero-Raspberry-Pi-Analogue-to-Digital-converter)
5V from board Vcc used in voltage divider with 9.4 k ohm and the thermister.
TODO, electrical implementation should use a voltage reference instead of 5V
from the board.

### Deploy logger

    $ ansible-playbook deploy/playbook_temperature_sensor.yml -i private/deploy/inventory

### Start logger

    raspberrypi:~ $ nohup python3 -m monitor_actuator.src.temperature_sensor.log_temperature &


## Tests

    $  PYTHONPATH=`pwd` pytest tests/**/* --pdb

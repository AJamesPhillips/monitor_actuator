
# Monitor Actuator

A repo to contain code and instructions for setting up and running a system for
monitoring and actuating (MA - pronounced 'M' 'A').

Example use cases include:

  * Temperature monitor(s) for warning fridge/freezer failure
  * Webcam(s) for taking periodic photos of the lab as extra aids to protecting
    the occupants and the space, as well as potential usage stats to inform
    debate
  * Sense RFID
  * Enable / disable equipment e.g. for maintenance, access control or safety

## Description of system

    * The system contains many nodes
        * Each node is some form of networked computer
            * The nodes described here are Raspberry Pi Zero with WiFi USB dongles for
              connectivity.  Other hardware/roles will need different provisioning scripts.
        * There can be multiple functions performed by one node.
        * There can be multiple users able to access different nodes.
    * A central server allows access to all nodes (via reverse SSH tunnelling).
        * even if the node's network lacks a public static IP address (Does not
          yet work on networks that restriction ssh, such as some university or
          corporate networks).

## Getting started

### Clone the repo

    $ git clone --recursive git@github.com:AJamesPhillips/monitor_actuator.git
    $ git submodule update --init --recursive  # update the repo submodules

### Customisation / private credentials / configuration

The private directory contains all your customisation / private credentials /
configuration for your system.

    private$ python setup_private.py  # copies templates for you to correct file locations
    private$ git init

Or if you have an existing repo with credentials / config:

    $ rm -rf private
    $ git clone git@yourrepo.com private
    $ git checkout private

### What you will need

#### Basic node

  - [ ] 1x Raspberry Pi Zero
  - [ ] 1x micro SD card (8 Gb or more)
  - [ ] 1x USB WiFi dongle
  - [ ] 1x female USB to male micro USB B adapter or cable
  - [ ] 1x mains to 5V DC power supply with male micro USB B cable

Only needed for set up

  - [ ] 1x micro to full SD card adapter
  - [ ] 1x male USB to male micro USB B cable
  - [ ] \(Optional: 1x monitor with HDMI\)
  - [ ] \(Optional: 1x HDMI cable\)
  - [ ] \(Optional: 1x HDMI to mini HMDI adapter\)
  - [ ] \(Optional: 1x keyboard & USB to micro USB B adapter\)
  - [ ] \(Optional: 1x powered USB bus with 2 spaces\)

### Provisioning & deployment

Uses Ansible.

#### Activate Ansible

    $ virtualenv --python=/usr/bin/python2.7 venv
    $ source ./venv/bin/activate
    $ pip install -r deploy/ansible/requirements.txt
    $ source deploy/ansible/hacking/env-setup
    $ cd deploy

### Bootstrapping

See BOOTSTRAPPING.md

## Deploying

### Deploy e.g. temperature loggers

    deploy$ ansible-playbook playbook.yml -i ../private/deploy/inventory

### Deploy just one node

    deploy$ ansible-playbook playbook.yml -i ../private/deploy/inventory --limit "<your-node-name>"

## Debugging

Sometimes you want to track what the node is doing.
ssh onto the node
Then:

    cd /home/pi/monitor_actuator
    tail -f *.log

To find out if your node is making connections to the outside world:

    netstat -a  # show all current connections
    ping ma-node04.local  # find the ip address of your local node
    arp -a  # list all devices on local network

To kill a hanging connection (from: https://superuser.com/a/668155/148811)

    netstat -np  # Will need to be root user.  Under `PID/Program name` take the PID. e.g. from `650/python3` take 650.  Use as $pid below:
    lsof -np $pid  # May need to apt-get install lsof.  This prints out a list.  Get the corresponding file descriptor.  E.g. from this:
    python3 650 root    4u  IPv4 668333      0t0    TCP 192.160.0.1:40000->123.45.67.190:https (ESTABLISHED)
    Take the `4u` as the file descriptor.
    gdb -p $pid
    call close($fileDescritor)
    quit

### Recovering data

You can bisect to find the start and end of when the data was being dropped:

    dd skip=77590 count=1 if=temperature.log of=temperature.log-2 bs=4096 && grep CERTIFICATE_VERIFY_FAILED temperature.log-2

Extract into a file, parse and upload to db:

    dd skip=189453 count=51377 if=temperature.log of=temperature.log-to-recover bs=4096
    # Copy parse-temp-log.py to the node from the ./scripts directory
    python3 parse-temp-log.py
    # Copy it off the node and to local
    rsync --progress your-node-user@ma-node01:/home/pi/monitor_actuator/recovered-temp-data ./recovered-temp-data
    # Copy it from local to server for further processing
    rsync --progress ./recovered-temp-data your-server-user@your-server.com:/home/server-user/recovered-temp-data

## TODO

  - [ ] Reimplement reverse ssh tunnel and cron refresh
  - [ ] Implement autogeneration of ssh_auto_generated.cfg file

### TODO automate provisioning of MA_NODE(s):

- [ ] Use https://github.com/pinkeen/ansible-role-ssh-tunnel-client
- [ ] if not present in /etc/monitor_actuator/MA_NODE_UUID,  set MA_NODE_UUID number to NEXT_MA_NODE_UUID and
- [ ]     increment (by 2) and update NEXT_MA_NODE_UUID in local provision repo
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



## Tests

    $  PYTHONPATH=`pwd` pytest tests/**/* --pdb

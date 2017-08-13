
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

    private$ python setup_private.py
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

### Automated provisioning

Uses Ansible.

#### Activate Ansible

    $ source deploy/ansible/hacking/env-setup
    $ cd deploy

## Set up (Provisioning)

This will get a Raspberry Pi Zero from nothing to being a node you can
(amongst other things):
  * SSH into locally via USB (and WiFi) on the hostname you specify
  * SSH in using your public-private key
  * Have your own personal user account on the node (useful for access
  control and later auditing for maintenance or security)
  * Provision the node with any functionality you need.

### Bootstrap step 1: Install OS and access via USB cable

#### Format SD card

We use Raspbian Jessie Lite [from here](https://www.raspberrypi.org/downloads/raspbian/).
Currently tested on:
  * Linux raspberrypi 4.4.38+ #938 Thu Dec 15 15:17:54 GMT 2016 armv6l GNU/Linux

  - [ ] Download the .zip, unzip to get the .img file
  - [ ] Card mount location.  Find where your card is mounted:
    * On Mac OSX
      - [ ] Open a terminal and type `diskutil list`
      - [ ] Insert the SD card
      - [ ] Wait a few seconds, type `diskutil list` again in the terminal window
      and make a note of the identifier of the new entry.  It should be
      something like `/dev/disk2`.  This is where your SD card is mounted
  - [ ] [Format the SD card](https://www.andrewmunsell.com/blog/raspberry-pi-noobs-tutorial/)
    - [ ] On Mac OSX run "Disk Utility" and erase the SD card.  Remember to
    **select the root** of the card and choose **MS-DOS(FAT)**.  If it does not
    show three options with the third listing "Master Boot Record" you have not
    selected the root of the card.  Give it any name you like
    - [ ] On Windows you may want to use the
    [SD Card Formatter](https://www.sdcard.org/downloads/formatter_4/).
    TODO test this.

#### Copy Raspberry Pi OS onto SD card

Make sure `Activate Ansible` instructions above have been followed.
Replace `</Full/path/to/disk>` with the value from `Card mount location` above and
`</Full/path/to/raspbian-jessie-lite.img>` from the download section.

Note: This only works on Mac OSX at this time but should be easy to update for
Windows.

Note: This will modify files on `/Volumes/boot`.  Do not run this command if
you already have a volume here and do not want it modified.

    deploy$ ansible-playbook playbook_bootstrap1_sd_card.yml -i "localhost," -e "disk=</Full/path/to/disk> img_file=</Full/path/to/raspbian-jessie-lite.img>" --ask-become-pass --connection=local

#### Boot up the Pi

  - [ ] Take out the SD card from your computer
  - [ ] Put the micro SD card into the Raspberry Pi Zero
  - [ ] Connect a USB cable from your computer to the USB **not the PWR** micro
  USB B connector on the Pi.  Optionally attach the HMDI cable.
  - [ ] The green light on the Pi should blink.  If the screen is attached it
  should turn on with various messages such as 'Resized root filesystem' etc.
  - [ ] Wait for ~2 minutes for the initial set up to run.
  - [ ] In a terminal type: `ssh pi@raspberrypi.local`.
        (It may give you a message such as: `The authenticity of host 'raspberrypi.local ... can't be established.`
        to which you can chose yes.  Alternatively if you have already connected
        to a different raspberrypi before it will just hang and you will need to
        remove it's entry from your `~/.ssh/known_hosts` file and retry.)
  - [ ] When prompted for `password` use `raspberry`
        These are temporary access credentials and will change shortly once
        you've completed provisioning.

It has worked if you are presented with the command line `pi@raspberrypi:~ $` or something similar.

### Bootstrap step 2: Change hostname

#### Specifying node name (hostname(s))

  - [ ] In `private/deploy/inventory` change `<name-of-node>` to something
  like node01 or door-ma, etc. As mentioned in the comment in that file, names
  can only have letters, digits or hyphens, and must start with a letter, nothing
  else is allowed.
  - [ ] Use the same name in the command below

    deploy$  ansible-playbook playbook_bootstrap2_hostname.yml -u pi -k -i raspberrypi.local, -e "new_hostname=<name-of-node>"

TODONEXT describe/automate adding to inventory and ~/.ssh/config  (Or skip
doing this for the moment as it should become obvious later what we need to do.
i.e. currently I'm not sure how you can access it locally, AND
via the control server.  Also need to add section on specifying what/where the
control server is).

          Host ma_node1
              HostName localhost
              User pi
              IdentityFile /controlpoint/.ssh/key
              Port 22222

### Bootstrap step 3: Access via Wifi with user credentials

### Access Pi over WiFi and give it access to internet

You will want to gain access to the Pi and for it to have access to the
internet over your and other local networks.

  - [ ] Edit the `./private/deploy/vars/networks.yml`.  The `<WiFi ESSID>`
  is the name of your WiFi network which you can get from your computers
  network settings.  You'll also need the networks password to replace
  `<WiFi Password>`.

deploy$  ansible-playbook playbook_bootstrap3_wifi.yml -u pi -k -i raspberrypi.local, -e "new_hostname=<name-of-node>"

#### Users and access permissions

TODO describe adding to private/deploy/public_keys and /vars/user_access.yml

You'll need to type in the password of `raspberry`

    deploy$  ansible-playbook playbook_bootstrap.yml -u pi -k -i raspberrypi.local, -e "new_hostname=<new-host-name> wifi_essid=<WiFi ESSID> wifi_pass=<WiFi Password>"

  - [ ] Follow the instructions and add a ~/.ssh/config for this new node
  - [ ] Test it works, `ssh <new-host-name>` should prompt you
  for the password again.

TODONEXT, add this to the playbook_bootstrap.yml
sudo sh -c "wpa_passphrase <WiFi ESSID> <WiFi Password> | sed '/#psk/d' >> /etc/wpa_supplicant/wpa_supplicant.conf"



###



What this should achieve:
  * Set up different users and install their public keys for ssh access
  * Change the default password for the pi login
  * Set up USB access
  * Set up SSH reverse tunnel access to central server
  * Provision any other functionality such as temperature sensing

  <!--* If you'd like to permanently change the hostname from raspberrypi to
  something else use `sudo vi /etc/hostname` and `sudo vi /etc/hosts` to edit
  them to your different hostnames.  `sudo reboot` and then from your computer
  `ssh pi@<your new hostname>.local`.

#### Config connection via USB

Probably not needed as local WiFi networks are usually very stable.

If you have a Raspberry Pi Zero we can
[configure it to be connectable over USB](http://blog.gbaman.info/?p=791),
otherwise continue and follow the instructions for "WiFi internet access for
the Pi" later.

  * Reinsert the SD card in your computer
  * Edit the `config.txt` in the top level directory to add the new line
  `dtoverlay=dwc2`.  Save the file.
  * Edit `cmdline.txt` add ` modules-load=dwc2,g_ether` after `... rootwait` to
  give: `... rootwait modules-load=dwc2,g_ether`.  Save the file.
  * In the `/boot` directory add an empty file called `ssh`.-->





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



### Deploy e.g. temperature logger

    $ cd deploy
    deploy$ ansible-playbook playbook_temperature_sensor.yml -i ../private/deploy/inventory

### Start logger

    raspberrypi:~ $ nohup python3 -m monitor_actuator.src.temperature_sensor.log_temperature &


## Implementations

### Temperature logger

#### Option 1: ADC

Built for raspberry pi zero with [ADC board from ABElectronics](https://www.abelectronics.co.uk/p/69/ADC-Pi-Zero-Raspberry-Pi-Analogue-to-Digital-converter)
5V from board Vcc used in voltage divider with 9.4 k ohm and the thermister.
TODO, electrical implementation should use a voltage reference instead of 5V
from the board and or use a Wheatstone bridge.

#### Option 2: Digital DS18B20

1-Wire DS18B20
Buy from ebay, £11 for 5: [5pcs DS18b20 Waterproof Temperature Sensor Thermal Probe Thermometer Durable 2M](http://www.ebay.co.uk/itm/162158276878)
Using these instructions
Wire up RED=Vcc BLACK=GND WHITE/YELLOW=SIG so that Vcc is 5V supply and Sig is GPIO4
Add lines to end of /etc/modules:
w1-gpio
w1-therm



## Tests

    $  PYTHONPATH=`pwd` pytest tests/**/* --pdb

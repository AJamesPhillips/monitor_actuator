# Add helper script

vi /usr/local/bin/safe-shutdown

        #!/bin/bash
        (sleep 2 && sudo shutdown now &); exit;

chmod +x /usr/local/bin/safe-shutdown

vi /usr/local/bin/safe-reboot

        #!/bin/bash
        (sleep 2 && sudo shutdown --reboot now &); exit;

chmod +x /usr/local/bin/safe-reboot


# Set up node and central server

## On the node

    ssh ma-node05
    passwd -dl pi

    sudo su root
    useradd -m --groups sudo --shell /bin/bash central01
    su central01
    passwd -dl central01
    mkdir ~/.ssh
    ssh-keygen -t rsa -b 4096
    vi ~/.ssh/config
        Host ma-central01
            HostName 142.93.39.216
            User node05
            IdentityFile ~/.ssh/id_rsa

## On central server

    ssh ma-central01

    sudo su root
    useradd -m --shell /bin/bash node05
    passwd -dl node05
    su node05
    mkdir ~/.ssh
    touch ~/.ssh/authorized_keys


    exit
    su www-data -s /bin/bash
    mkdir ~/.ssh
    ssh-keygen -t rsa -b 4096
    vi ~/.ssh/config
        Host ma-node05
            Hostname localhost
            Port 20200
            User central01
            IdentityFile ~/.ssh/id_rsa

## On both:

    # Copy ~/.ssh/id_rsa.pub from node05 to /var/www/.ssh/authorized_keys (on central server)
    cat ~/.ssh/id_rsa.pub
    # Copy ~/.ssh/id_rsa.pub from central server to ~/.ssh/authorized_keys (on node05)

# Set up robust and auto starting ssh tunnel
Copied from: https://superuser.com/questions/37738/how-to-reliably-keep-an-ssh-tunnel-open#comment1941840_1105956

    ssh ma-node05
    sudo su root
    vi /etc/systemd/system/ssh-tunnel-central01.service
    # Put in the content:
        [Unit]
        Description=SSH Reverse Tunnel into Central Server 01
        After=network.target

        [Service]
        Restart=always
        RestartSec=20
        User=central01
        # Don't use the "-f" flag as we keep the process going
        ExecStart=/usr/bin/ssh -o TCPKeepAlive=yes -o ServerAliveInterval=5 -o ServerAliveCountMax=1 -N -T -R20200:localhost:22 ma-central01

        [Install]
        WantedBy=multi-user.target

    systemctl enable ssh-tunnel-central01

    # or to update:
    systemctl status ssh-tunnel-central01
    systemctl daemon-reload

## Debugging

journalctl -f | grep ssh
service ssh-tunnel-central01 status

### On node05:

To start a connection:

    ssh -o TCPKeepAlive=yes -o ServerAliveInterval=5 -o ServerAliveCountMax=1 -f -N -T -R20200:localhost:22 ma-central01

To view the sshd logs:

    sudo grep 'sshd' /var/log/auth.log

### On the server

    ssh -p 20200 central@localhost






# To get Raspberry pi to talk serially with Arduino:

        $ dmesg | grep "console \[tty"
        # shows: console [ttyAMA0] enabled
        sudo raspi-config
        # "Interfacing Options" -> "Serial"
        # "Would you like a login shell to be accessible over serial?" => No
        #  Would you like the serial port hardware to be enabled? => Yes
        # reboot
        # /boot/config.txt should now have `enable_uart=1`
                        # apt-get install wiringpi # not needed?
        apt-get install python3-serial

        sudo su central
        vi /home/central/read_serial.py
                #!/usr/bin/env python3
                import serial
                import sys

                baudrate = int(sys.argv[1]) if len(sys.argv) > 1 else 9600
                print("Running at baudrate: " + str(baudrate))

                ser = serial.Serial(
                        port='/dev/ttyAMA0',
                        baudrate = baudrate,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=None
                )

                try:
                        while True:
                                x = ser.readline()
                                print(x)

                except KeyboardInterrupt as e:
                        print("KeyboardInterrupt stopping read_serial")

        chmod +x /home/central/read_serial.py
        vi /home/central/write_serial.py
                #!/usr/bin/env python3
                import serial
                import sys

                baudrate = int(sys.argv[1]) if len(sys.argv) > 1 else 9600
                print("Running at baudrate: " + str(baudrate))
                message = sys.argv[2] if len(sys.argv) > 2 else None

                ser = serial.Serial(
                        port='/dev/ttyAMA0',
                        baudrate = baudrate,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=None
                )

                try:
                        while True:
                                if message:
                                        x = message
                                else:
                                        x = input()
                                ser.write(x.encode('utf-8'))
                                if message:
                                        break

                except KeyboardInterrupt as e:
                        print("KeyboardInterrupt stopping write_serial")


        chmod +x /home/central/write_serial.py
        ./read_serial.py 9600
        ./write_serial.py 9600

## Debug

        python3 -m serial.tools.miniterm /dev/ttyAMA0 9600  # Do this first to set baudrate
        echo "hello" > /dev/ttyAMA0


# To set up cron for taking pictures
    ssh ma-node05
    sudo su central01
    cd /home/central01
    mkdir -P timelapse/photos
    cd timelapse
    touch take_photo.py
    chmod +x take_photo.py

edit take_photo.py to have:
    #!/usr/bin/env python3
    import subprocess
    import os
    from datetime import datetime
    from time import sleep

    cd = os.path.dirname(os.path.realpath(__file__))

    def subprocess_error(cmd):
        subprocess.check_output(
            cmd,
            shell=True
        )

    def take_photo(fatal_on_error = False):
        successful = False

        try:
            print("Take photo: attempt")
            date = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            subprocess_error("sudo raspistill -o {}/photos/{}.jpg".format(cd, date))
            subprocess_error("sudo chown -R central01:central01 {}/photos/*".format(cd))
            print("Take photo: success")
            successful = True
        except Exception as e:
            print("Take photo: failure: {}".format(e))
            if (fatal_on_error):
                raise e

        return successful

    def retry_take_photo(retries):
        while (retries > 0):
            fatal_on_error = not(bool(retries))
            if (take_photo()):
                return
            retries -= 1

            print("Sleeping before retrying, retries left: {}".format(retries))
            sleep(10)

    retry_take_photo(2)

cron job:
    crontab -e

    0,15,30,45 * * * * /home/central01/timelapse/take_photo.py

## Debug
    sudo grep CRON /var/log/syslog


# From central get video stream from node to central

        ssh ma-central01
        sudo apt-get install cvlc
        sudo su www-data -s /bin/bash
        # once on ma-central01:
        ssh ma-node05 "sudo raspivid -o - -t 0 -w 800 -h 400 -fps 24" | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8162}' :demux=h264
        # from computer:
        # open vlc, then "File" > "Open network" > enter the url "https://xeno.bio/video/8162/" (previously "http://142.93.39.216:8162")


## Debugging:

        # from computer:
        ssh ma-node05
        # on node05
        sudo su central
        sudo raspivid -o - -t 0 -hf -w 800 -h 400 -fps 24 | ssh central "cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8162}' :demux=h264"




# https://raspberrypi.stackexchange.com/questions/7446/how-can-i-stream-h-264-video-from-the-raspberry-pi-camera-module-via-a-web-serve

# hf to mirror horizontally
        sudo raspivid -o - -t 0 -hf -w 800 -h 400 -fps 24 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264


# Find how the tty is set up:
stty -F /dev/ttyAMA0 -a
speed 9600 baud; rows 0; columns 0; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>; eol2 = <undef>; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O;
min = 1; time = 0;
-parenb -parodd -cmspar cs8 hupcl -cstopb cread clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc -ixany -imaxbel -iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc


python3 -m serial.tools.miniterm /dev/ttyAMA0 9600



import time

def write(msg, delay):
  for char in msg:
    with open("/dev/ttyAMA0", "w") as f:
      f.write(char)
      time.sleep(delay)

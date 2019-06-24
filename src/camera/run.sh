# Set up node and central server

## On the node

    ssh node05
    passwd -dl pi

    sudo su root
    useradd -m --groups sudo --shell /bin/bash central
    passwd -dl central
    su central
    mkdir ~/.ssh
    ssh-keygen -t rsa -b 4096
    touch ~/.ssh/config
        Host central
            HostName 142.93.39.216
            User node05
            IdentityFile ~/.ssh/id_rsa

## On central server

    ssh rtsp01
    useradd -m --shell /bin/bash node05
    passwd -dl node05
    su node05
    mkdir ~/.ssh
    ssh-keygen -t rsa -b 4096
    touch ~/.ssh/authorized_keys
    touch ~/.ssh/config
        Host ma-node05
            Hostname localhost
            Port 20200
            User central
            IdentityFile ~/.ssh/id_rsa

## On both:

    # Copy ~/.ssh/id_rsa.pub from node05 to ~/.ssh/authorized_keys (on central server)
    cat ~/.ssh/id_rsa.pub
    # Copy ~/.ssh/id_rsa.pub from central server to ~/.ssh/authorized_keys (on node05)

## On node05:

    ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=1 -f -N -T -R20200:localhost:22 central

## On the server

    ssh -p 20200 central@localhost

# Set up robust and auto starting ssh tunnel
Copied from: https://superuser.com/questions/37738/how-to-reliably-keep-an-ssh-tunnel-open#comment1941840_1105956

    ssh ma-node05
    sudo su root
    touch /etc/systemd/system/ssh-tunnel-central.service
    # Put in the content:
        [Unit]
        Description=SSH Reverse Tunnel into Central Server
        After=network.target

        [Service]
        Restart=always
        RestartSec=20
        User=central
        # Don't use the "-f" flag as we keep the process going
        ExecStart=/usr/bin/ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=1 -N -T -R20200:localhost:22 central

        [Install]
        WantedBy=multi-user.target

    systemctl enable ssh-tunnel-central

## Debugging

journalctl -f | grep ssh
service ssh-tunnel-central status





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
                                x = input()
                                ser.write(x.encode('utf-8'))

except KeyboardInterrupt as e:
        print("KeyboardInterrupt stopping write_serial")


        chmod +x /home/central/write_serial.py
        ./read_serial.py 9600
        ./write_serial.py 9600


## Debug

        python3 -m serial.tools.miniterm /dev/ttyAMA0 9600  # Do this first to set baudrate
        echo "hello" > /dev/ttyAMA0


# From central get video stream from node to central

        ssh central
        # once on central:
        ssh ma-node05 "sudo raspivid -o - -t 0 -hf -w 800 -h 400 -fps 24" | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8162}' :demux=h264
        # from computer:
        # open vlc, then "File" > "Open network" > enter the url "http://142.93.39.216:8162"

# Publish the video stream

        ssh rtsp01
        sudo apt-get install nginx
        # NOTE: there is an nginx file with the following
        # BUT I DON'T THINK WE NEED IT
        /etc/nginx/conf.d$ cat proxy_stream.conf
        server {
            listen 8160;
            server_name 142.93.39.216;

            location / {
                proxy_pass http://localhost:8161;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_read_timeout 90s;
            }
        }








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

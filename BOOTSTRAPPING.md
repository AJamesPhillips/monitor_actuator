

# Bootstrapping / set up / provisioning

This will get a Raspberry Pi Zero from nothing to being a node you can
(amongst other things):
  * SSH into locally via USB (and WiFi) on the hostname you specify
  * SSH in using your public-private key
  * Have your own personal user account on the node (useful for access
  control and later auditing for maintenance or security)
  * Provision the node with any functionality you need.

## Bootstrap step 1: Install OS and access via USB cable

### Format SD card

We use Raspbian Lite [from here](https://www.raspberrypi.org/downloads/raspbian/).
Currently tested on:
  * Linux raspberrypi 4.4.38+ #938 Thu Dec 15 15:17:54 GMT 2016 armv6l GNU/Linux (Raspian Jessie Lite)
  * 4.14 2019-04-08  (Raspian Stretch Lite)

  - [ ] Download the .zip, unzip to get the .img file
  - [ ] Card mount location.  Find where your card is mounted:
    * On Mac OSX
      - [ ] Open a terminal and type `diskutil list`
      - [ ] Insert the SD card
      - [ ] Wait a few seconds, type `diskutil list` again in the terminal window
      and make a note of the identifier of the new entry.  It should be
      something like `/dev/disk2`.  This is where your SD card is mounted
  - [ ] [Format the SD card](https://www.andrewmunsell.com/blog/raspberry-pi-noobs-tutorial/)
    - [ ] On Mac OSX run `diskutil eraseDisk FAT32 NEWNODE /dev/disk2`
    - [ ] Alternatively run "Disk Utility" and erase the SD card.  Remember to
    **select the root** of the card and choose **MS-DOS(FAT)**.  You may need to select:
    "View -> Show all devices"  If it does not
    show three options with the third listing "Master Boot Record" you have not
    selected the root of the card.  Give it any name you like
    - [ ] On Windows you may want to use the
    [SD Card Formatter](https://www.sdcard.org/downloads/formatter_4/).
    TODO test this.

### Copy Raspberry Pi OS onto SD card

Make sure `Activate Ansible` instructions in README.md have been followed.
Replace `</Full/path/to/disk>` with the value from `Card mount location` above and
`</Full/path/to/raspbian-jessie-lite.img>` from the download section.

Note: This only works on Mac OSX at this time but should be easy to update for
Windows.

Note: This will modify files on `/Volumes/boot`.  Do not run this command if
you already have a volume here and do not want it modified.

    deploy$ ansible-playbook playbook_bootstrap1_sd_card.yml -i "localhost," -e "disk=</Full/path/to/disk> img_file=</Full/path/to/raspbian-jessie-lite.img>" --ask-become-pass --connection=local

### Boot up the Pi

  - [ ] Take out the SD card from your computer
  - [ ] Put the micro SD card into the Raspberry Pi Zero
  - [ ] Connect a USB cable from your computer to the USB **not the PWR** micro
  USB B connector on the Pi.  Optionally attach the HMDI cable.
  - [ ] The green light on the Pi should blink.  If the screen is attached it
  should turn on with various messages such as 'Resized root filesystem' etc.
  - [ ] Wait for ~2 minutes for the initial set up to run.
  - [ ] In a terminal type: `ssh pi@raspberrypi.local`.
      * Trouble Shooting 1: It may give you a message such as: `The authenticity
        of host 'raspberrypi.local ... can't be established.`
        to which you can chose yes.
      * Trouble Shooting 2: Alternatively if you have already connected
        to a different raspberrypi before it will just hang and you will need to
        remove it's entry from your `~/.ssh/known_hosts` file and retry.
      * Trouble Shooting 3: Finally
        it may also hang if you are connected to wifi and have other raspberry pis
        on there (?), if so: disconnect the wifi, then you will be able to run
        `ssh pi@raspberrypi.local`, issue the command `(sleep 2 && sudo shutdown -r now &); exit`, when
        the green light turns off, turn back on WiFi, unplug and replug the usb
        cable and you should be able to ssh into it successfully.)
  - [ ] When prompted for `password` use `raspberry`
        These are temporary access credentials and will change shortly once
        you've completed provisioning.

It has worked if you are presented with the command line `pi@raspberrypi:~ $` or something similar.

## Bootstrap step 2: Change hostname

### Specifying node name (hostname(s))

  - [ ] Copy `private/deploy/inventory.template` to `private/deploy/inventory`
  - [ ] In `private/deploy/inventory` change `<name-of-node>` to something
  like node01 or door-ma, etc. As mentioned in the comment in that file, names
  can only have letters, digits or hyphens, and must start with a letter, nothing
  else is allowed.
  - [ ] Use the same name in the command below

    `deploy$  ansible-playbook playbook_bootstrap2_hostname.yml -u pi --connection paramiko -k -i raspberrypi.local, -e "new_hostname=<name-of-node>"`

Trouble Shooting 1: when you run this command, if you receive an error under the `TASK [Gathering Facts]` task like:

    fatal: [your-node-name.local]: UNREACHABLE! => {"changed": false, "msg": "timed out", "unreachable": true}

Retry the command first.  Failing that check you can log into the node over ssh
with `ssh pi@raspberrypi.local`, then retry the command above.

## Bootstrap step 3: Access via Wifi with user credentials

## Give the node access to internet and access it over WiFi

You will want to gain access to the Pi and for it to have access to the
internet over your local and other networks.  Additionally you need to secure it
by removing the default authentication credentials and replacing with user names
and public keys

  - [ ] Edit `./private/deploy/vars/networks.yml`.  The `<WiFi ESSID>`
  is the name of your WiFi network which you can get from your computers
  network settings.  You'll also need the networks password to replace
  `<WiFi Password>`.
  - [ ] Add your public key to `./private/deploy/public_keys/`.
  - [ ] Edit `./private/deploy/vars/user_access.yml`

    `deploy$  ansible-playbook playbook_bootstrap3_wifi.yml -u pi --connection paramiko -k -i <name-of-node>.local,`

After copying the `potential_ssg_config.tmp` to your `~/.ssh/config`, check it has
work with:  `$ ssh <name-of-node>`  It should **not** prompt you for a password.

## Bootstrap step 4: Disable login to via password

    deploy$  ansible-playbook playbook_bootstrap4_secure.yml -i <name-of-node>.local,

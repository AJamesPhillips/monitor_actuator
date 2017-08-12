


## Remove notes regarding manual steps now avoided, or automated
### Copy OS onto SD card

  - [ ] Copy the Raspbian OS image onto the SD card.
    * On Mac OSX
      - [ ] In the terminal unmount the disk using
      `diskutil unmountDisk /dev/<disk>` where <disk> is replaced by the SD
      mounting location such as `disk2`
      - [ ] Copy image file onto the disk:

        `$ sudo dd bs=16m if=<your image file>.img of=/dev/<disk>`

        This may take a while, either use
      ctrl + T or `kill -INFO $PID` to get progress info.
      - [ ] Unmount from finder (should now be listed as 'boot')

### Get your network ESSID (its name)

If you have connected the keyboard and USB WiFi dongle:

  - [ ] Login (see above)
  - [ ] Run `sudo iwlist wlan0 scan | grep ESSID`.  Find the ESSID that matches
  your local network.

If you don't have the USB WiFi dongle attached yet then get your
networks ESSID name from your computers network settings.

### Add network credentials and enable ssh access

  - [ ] Run the following replacing `<WiFi ESSID>` and `<WiFi Password>`
  [[1]](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)
  [[2]](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=114286)

    `$  sudo sh -c "wpa_passphrase <WiFi ESSID> <WiFi Password> | sed '/#psk/d' >> /etc/wpa_supplicant/wpa_supplicant.conf"`

### Test you can access Pi over WiFi

  - [ ] Unplug the keyboard and replace the with WiFi USB Dongle.  Optionally also
  unplug the mini HDMI.
  - [ ] Power cycle it (unplug and replug the USB power cable).  Wait for it to
  boot (about a 40 seconds).
  - [ ] Try to run the command `ssh pi@raspberrypi.local`, if you are prompted for
  a password, success!  (It may give you a message such as:
  `The authenticity of host 'raspberrypi.local ... can't be established.`
  to which you can chose yes.)

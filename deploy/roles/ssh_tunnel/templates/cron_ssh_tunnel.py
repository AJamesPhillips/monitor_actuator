#!/usr/bin/python3

# Note, changed this script from the original bash script as python just works.
# For example:
# http://stackoverflow.com/questions/42468182 and
# http://stackoverflow.com/questions/42488773

import re
from time import sleep
from subprocess import call, Popen, PIPE


with Popen(["ps", "-eo", "pid,args"], stdout=PIPE) as proc:
    ssh_processes = proc.stdout.read().decode('ascii')

ssh_details = "{{ REMOTE_PORT }}:localhost:22 {{ REMOTE_USER }}@{{ REMOTE_IP }}"
pids = re.findall('^[ ]*(\d+).*{}.*$'.format(ssh_details), ssh_processes, re.MULTILINE)

# kill old ssh process(es)
for pid in pids:
    print("Killing old ssh process: {}".format(pid))
    with Popen(["kill", pid], stdout=PIPE) as proc:
        killed = proc.stdout.read().decode('ascii')

sleep(1)

# set up ssh
call(["ssh -f -N -T -R{} -i /home/pi/.ssh/raspberrypi01".format(ssh_details)], shell=True)

sleep(1)

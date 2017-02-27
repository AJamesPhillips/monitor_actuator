
#!/bin/sh

{% set PID_FILE=CRON_DIR ~ SSH_TUNNEL_NAME ~ ".pid" %}
touch {{ PID_FILE }}
# kill old ssh process
kill `cat {{ PID_FILE }}`
sleep 1

# set up ssh
ssh -f -N -T -R{{ REMOTE_PORT }}:localhost:22 {{ REMOTE_USER }}@{{ REMOTE_IP }} -i /home/pi/.ssh/raspberrypi01
# record new pid
ps -eo pid,args | grep -Po "^\d+(?= .*[R]{{ REMOTE_PORT }}:localhost:22 {{ REMOTE_USER }}@{{ REMOTE_IP }})" > {{ PID_FILE }}

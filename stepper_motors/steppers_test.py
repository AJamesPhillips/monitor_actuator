#!/usr/bin/python
#
# Modified from :
# https://bitbucket.org/MattHawkinsUK/rpispy-misc/src/31bccbd8fe1022691d3003b38c3fb8e71d5a59a9/python/stepper.py?at=master&fileviewer=file-view-default
#
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#    Stepper Motor Test
#
# A simple script to control
# a stepper motor.
#
# Author : Matt Hawkins
# Date   : 28/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
StepPins = [
  [17,18,27,22],
  [23,24,25,4],
  [13,12,6,5],
  [20,26,16,19]
]


# Set all pins as output
for pinGroup in StepPins:
  for pin in pinGroup:
    print "Setup pins"
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]

StepCount = len(Seq)
StepDir = 1 # Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise

# Read wait time from command line
if len(sys.argv)>1:
  WaitTime = int(sys.argv[1])/float(1000)
else:
  WaitTime = 10/float(1000)

if len(sys.argv) > 2:
  StepDir = int(sys.argv[2])
  print "StepDir set to: {}".format(StepDir)
else:
  StepDir = 1

# Initialise variables
StepCounter = 0

try:
  # Start main loop
  while True:

    # print StepCounter,
    # print Seq[StepCounter]

    for pinGroup in StepPins:
      for ipin, pin in enumerate(pinGroup):
        activity = Seq[StepCounter][ipin] == 1
        # print "set GPIO {} to {}".format(pin, activity)
        GPIO.output(pin, activity)

    StepCounter += StepDir

    # If we reach the end of the sequence
    # start again
    if (StepCounter>=StepCount):
      StepCounter = 0
    if (StepCounter<0):
      StepCounter = StepCount+StepDir

    # Wait before moving on
    time.sleep(WaitTime)

except:
  print "Exiting, setting pins to 0"
  for pinGroup in StepPins:
    for pin in pinGroup:
      GPIO.output(pin, False)


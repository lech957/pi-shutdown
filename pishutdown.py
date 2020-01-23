#!/usr/bin/python
# shutdown/reboot(/power on) Raspberry Pi with pushbutton

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time

# pushbutton connected to this GPIO pin, using pin 5 also has the benefit of
# waking / powering up Raspberry Pi when button is pressed
shutdownPin = 5 #Pin 5 is GPIO 3 

# if button pressed for at least this long then shut down. if less then reboot.
shutdownMinSeconds = 6 # 6 seconds for shutdown

rebootMinSeconds = 2 # 2 seconds for reboot

#everything less than 2 seconds will cause a network service restart




# button debounce time in seconds
debounceSeconds = 0.01

GPIO.setmode(GPIO.BOARD)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonPressedTime = None

pasthToNicRestartScript='/home/alf/scripts/pi-shutdown/restart_nics.sh'

def buttonStateChanged(pin):
    global buttonPressedTime

    if not (GPIO.input(pin)):
        # button is down
        if buttonPressedTime is None:
            buttonPressedTime = datetime.now()
    else:
        # button is up
        if buttonPressedTime is not None:
            elapsed = (datetime.now() - buttonPressedTime).total_seconds()
            buttonPressedTime = None
            if elapsed >= shutdownMinSeconds:
                # button pressed for more than specified time, shutdown
                call(['shutdown', '-h', 'now'], shell=False)
            elif elapsed >= rebootMinSeconds:
                # button pressed for a shorter time, reboot
                call(['shutdown', '-r', 'now'], shell=False)

            elif elapsed >= debounceSeconds:
                # button pressed for a shorter time, reboot
                #call(['shutdown', '-r', 'now'], shell=False)
                #call the network restart script here
                call([pasthToNicRestartScript], shell=False)
                pass


# subscribe to button presses
GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged)

while True:
    # sleep to reduce unnecessary CPU usage
    time.sleep(5)

#!/usr/bin/env python3

import RPi.GPIO as GPIO
from datetime import datetime
import time

# setup some user variables
doorTravelTime = 5 # seconds allowed for the door to open or close

# initalize some flags and variables
openStep = 0
closeStep =0

# basackwards relay constants
RUN = False
STOP = True

# setup I/O Constants
DOOR_UP = 4
DOOR_DOWN = 5
DOOR_LOCK = 6
LIGHTS = 7
MAN_UP = 22
MAN_DOWN = 23
MAN_LIGHT = 24
UP_PROX = 26
DOWN_PROX = 27

# setup I/O
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DOOR_UP, GPIO.OUT) # Motor FWD
GPIO.output(DOOR_UP, STOP)
GPIO.setup(DOOR_DOWN, GPIO.OUT) # Motor REV
GPIO.output(DOOR_DOWN, STOP)
GPIO.setup(DOOR_LOCK, GPIO.OUT) # Door Lock
GPIO.output(DOOR_LOCK, STOP)
GPIO.setup(LIGHTS, GPIO.OUT) # Lights
GPIO.output(LIGHTS, STOP)
GPIO.setup(MAN_UP, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Manual Up Switch
GPIO.setup(MAN_DOWN, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Manual Down Switch
GPIO.setup(MAN_LIGHT, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Manual Light Switch
GPIO.setup(UP_PROX, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Door Up Switch
GPIO.setup(DOWN_PROX, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Door Down Switch

up = False
down = False

try:
	while True:
		if GPIO.input(MAN_UP) and not up:
			time.sleep(5)
			print('Up {} {}'.format(openStep, closeStep))
			up = True
			down = False
		if GPIO.input(MAN_DOWN) and not down:
			time.sleep(5)
			print('Down {} {}'.format(openStep, closeStep))
			down = True
			up = False

		if GPIO.input(MAN_UP) and openStep == 0: # Simulate door open time
			print('open step 0 starting {} {}'.format(openStep, closeStep))
			time.sleep(5)
			doorStartTime = datetime.now().timestamp()
			GPIO.output(DOOR_UP, RUN) # Door Open
			GPIO.output(DOOR_LOCK, RUN) # Door Lock
			print('open step 0 done {} {}'.format(openStep, closeStep))
			openStep = 1

		if openStep == 1: # test for door open or door time out
			if GPIO.input(UP_PROX):
				openStep = 2
			doorCurrentTime = datetime.now().timestamp()
			doorRunTime = doorCurrentTime - doorStartTime
			if doorRunTime > doorTravelTime:
				openStep = 3

		if openStep > 1:
			GPIO.output(DOOR_UP, STOP) # Door Open
			GPIO.output(DOOR_LOCK, STOP) # Door Lock

		if openStep == 2:
			doorIsOpen = True
			print('door is open {} {}'.format(openStep, closeStep))
			openStep = 4
			closeStep = 0

		if openStep == 3:
			doorTimeOut = True
			print('door up timed out {} {}'.format(openStep, closeStep))
			openStep = 4

		if GPIO.input(MAN_DOWN) and closeStep == 0: # the door should be closed
			time.sleep(5)
			doorStartTime = datetime.now().timestamp()
			GPIO.output(DOOR_DOWN, RUN) # Door Close
			GPIO.output(DOOR_LOCK, RUN) # Door Lock
			print('close step 0 done {} {}'.format(openStep, closeStep))
			closeStep = 1

		if closeStep == 1: # test for door closed or door time out
			if GPIO.input(DOWN_PROX):
				closeStep = 2
			doorCurrentTime = datetime.now().timestamp()
			doorRunTime = doorCurrentTime - doorStartTime
			if doorRunTime > doorTravelTime:
				closeStep = 3

		if closeStep > 1:
			GPIO.output(DOOR_DOWN, STOP) # Door Close
			GPIO.output(DOOR_LOCK, STOP) # Door Lock

		if closeStep == 2:
			doorIsClosed = True
			print('door is closed {} {}'.format(openStep, closeStep))
			closeStep = 4
			openStep = 0

		if closeStep == 3:
			doorTimeOut = True
			print('door down timed out {} {}'.format(openStep, closeStep))
			closeStep = 4


except KeyboardInterrupt:
	# here you put any code you want to run before the program
	# exits when you press CTRL+C
	print('\nKeyBoard Interrupt')

except Exception as e:
	# this covers all other exceptions
	print(str(e))

finally:
	GPIO.cleanup() # this ensures a clean exit

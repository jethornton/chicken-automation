#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep

# basackwards relay setup
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

try:
	upCnt = 0
	dnCnt = 0

	while True:
		# Manual Open Door
		# if the switch is on count up to 3
		if GPIO.input(MAN_UP) and upCnt < 3:
			upCnt += 1
		# if the switch is off count down to 0
		if not GPIO.input(MAN_UP) and upCnt > 0:
			upCnt -=1
		if GPIO.input(MAN_UP) and upCnt == 3:
			GPIO.output(DOOR_UP, RUN) # Door Open
			GPIO.output(DOOR_LOCK, RUN) # Door Lock
		if not GPIO.input(MAN_UP) and upCnt == 0:
			GPIO.output(DOOR_UP, STOP) # Door Open

		# Manual Close Door
		# if the switch is on count up to 3
		if GPIO.input(MAN_DOWN) and dnCnt < 3:
			dnCnt += 1
		# if the switch is off count down to 0
		if not GPIO.input(MAN_DOWN) and dnCnt > 0:
			dnCnt -=1
		if GPIO.input(MAN_DOWN) and dnCnt == 3:
			GPIO.output(DOOR_DOWN, RUN) # Door Open
			GPIO.output(DOOR_LOCK, RUN) # Door Lock
		if not GPIO.input(MAN_DOWN) and dnCnt == 0:
			GPIO.output(DOOR_DOWN, STOP) # Door Open

		if upCnt == 0 and dnCnt == 0:
			GPIO.output(DOOR_LOCK, STOP) # Door Lock



	sleep(0.1)

except KeyboardInterrupt:
	# here you put any code you want to run before the program
	# exits when you press CTRL+C
	print('\nKeyBoard Interrupt')

except Exception as e:
	# this covers all other exceptions
	print(str(e))

finally:
	GPIO.cleanup() # this ensures a clean exit

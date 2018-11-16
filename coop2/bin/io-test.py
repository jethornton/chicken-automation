#!/usr/bin/env python3

"""
GPIO.VERSION '0.6.3'
Raspberry Pi 3 Model B Rev 1.2

Input and Output testing program
"""

import RPi.GPIO as GPIO

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

# initalize some flags
doorManualUp = False
doorManualDown = False

try:
	while True:
		if GPIO.input(MAN_UP) and not GPIO.input(UP_PROX):
			GPIO.output(DOOR_UP, RUN) # Motor FWD
			GPIO.output(DOOR_LOCK, RUN) # Door Lock
			doorManualUp = True
		if GPIO.input(MAN_UP) and GPIO.input(UP_PROX):
			GPIO.output(DOOR_UP, STOP) # Motor FWD
			GPIO.output(DOOR_LOCK, STOP) # Door Lock
		if not GPIO.input(MAN_UP) and doorManualUp:
			GPIO.output(DOOR_UP, STOP) # Motor FWD
			GPIO.output(DOOR_LOCK, STOP) # Door Lock
			doorManualUp = False

		# manual Door Down
		if GPIO.input(MAN_DOWN) and not GPIO.input(DOWN_PROX):
			GPIO.output(DOOR_DOWN, RUN) # Motor REV
			GPIO.output(DOOR_LOCK, RUN) # Door Lock
			doorManualDown = True
		if GPIO.input(MAN_DOWN) and GPIO.input(DOWN_PROX):
			GPIO.output(DOOR_DOWN, STOP)
			GPIO.output(DOOR_LOCK, STOP)
		if not GPIO.input(MAN_DOWN) and doorManualDown:
			GPIO.output(DOOR_DOWN, STOP)
			GPIO.output(DOOR_LOCK, STOP)
			doorManualDown = False

		# Lights
		if GPIO.input(MAN_LIGHT):
			GPIO.output(LIGHTS, RUN)
		else:
			GPIO.output(LIGHTS, STOP)

except KeyboardInterrupt:
	# here you put any code you want to run before the program
	# exits when you press CTRL+C
	print('\nKeyBoard Interrupt')

except Exception as e:
	# this covers all other exceptions
	print(str(e))

finally:
	GPIO.cleanup() # this ensures a clean exit

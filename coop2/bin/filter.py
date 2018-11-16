#!/usr/bin/env python3

import RPi.GPIO as gpio
from time import sleep

# basackwards relay setup
RUN = False
STOP = True

# I/O constants
MAN_LIGHT = 24
LIGHTS = 7

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(MAN_LIGHT, gpio.IN,pull_up_down=gpio.PUD_DOWN) # Manual Light Switch
gpio.setup(LIGHTS, gpio.OUT) # Lights
gpio.output(LIGHTS, STOP)

mlCnt = 0
lights = False

try:
	while(not sleep(0.1)):
		# if the switch is on count up to 3
		if gpio.input(MAN_LIGHT) and mlCnt < 3:
			mlCnt += 1
		# if the switch is off count down to 0
		if not gpio.input(MAN_LIGHT) and mlCnt > 0:
			mlCnt -=1
		if mlCnt == 3 and not lights:
			gpio.output(LIGHTS, RUN)
			print('Da Lights are ON!')
			lights = True
		if mlCnt == 0 and lights:
			gpio.output(LIGHTS, STOP)
			print('Da Lights are OFF!')
			lights = False

except KeyboardInterrupt:
	# here you put any code you want to run before the program
	# exits when you press CTRL+C
	print('\nKeyBoard Interrupt')

except Exception as e:
	# this covers all other exceptions
	print(str(e))

finally:
	gpio.cleanup() # this ensures a clean exit


#!/usr/bin/env python3

import RPi.GPIO as gpio
from time import sleep

# basackwards relay setup
RUN = False
STOP = True

lt = 0

# I/O constants
MAN_UP = 22
MAN_DOWN = 23
MAN_LIGHT = 24
LIGHTS = 7

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(MAN_UP, gpio.IN,pull_up_down=gpio.PUD_DOWN) # Manual Up Switch
gpio.setup(MAN_DOWN, gpio.IN,pull_up_down=gpio.PUD_DOWN) # Manual Down Switch
gpio.setup(MAN_LIGHT, gpio.IN,pull_up_down=gpio.PUD_DOWN) # Manual Light Switch
gpio.setup(LIGHTS, gpio.OUT) # Lights
gpio.output(LIGHTS, STOP)

def manualUp(channel):
	print('Rising Edge detected on channel {}'.format(channel))

def manualDown(channel):
	print('Rising Edge detected on channel {}'.format(channel))

 # add rising edge detection on a channel
gpio.add_event_detect(MAN_UP, gpio.RISING, callback=manualUp, bouncetime=100)
gpio.add_event_detect(MAN_DOWN, gpio.RISING, callback=manualDown, bouncetime=100)


try:
	while(not sleep(0.1)):
		if gpio.input(MAN_LIGHT):
			lt += 1
		if lt == 10 and gpio.input(MAN_LIGHT):
			gpio.output(LIGHTS, RUN)
			print('Da Lights are ON!')
		if lt == 100 and gpio.input(MAN_LIGHT):
			gpio.output(LIGHTS, STOP)
			print('Timed Out!')
		if lt > 10 and not gpio.input(MAN_LIGHT):
			gpio.output(LIGHTS, STOP)
			lt = 0
			print('Da Lights are OFF!')


except KeyboardInterrupt:
	# here you put any code you want to run before the program
	# exits when you press CTRL+C
	print('\nKeyBoard Interrupt')

except Exception as e:
	# this covers all other exceptions
	print(str(e))

finally:
	gpio.cleanup() # this ensures a clean exit

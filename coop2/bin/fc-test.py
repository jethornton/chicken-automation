#!/usr/bin/env python3

from digole import lcd
import time
from datetime import datetime

timeFormat = '%I:%M %p'

s = lcd()

namedColors = {'black':0 , 'navy':2 , 'blue':3 , 'green':24 ,
'teal':27 , 'lime':28 , 'aqua':31 , 'maroon':192 , 'purple':195 ,
'olive':219 , 'red':224 , 'magenta':227 , 'yellow':252 , 'white':255}

try:
	while True:
		s.clearScreen()
		s.setForeColor('White')
		s.writeLine('Note: A Black')
		s.changePosition(0, 1)
		s.writeLine('foreground will not')
		s.changePosition(0, 2)
		s.writeLine('show up on a')
		s.changePosition(0, 3)
		s.writeLine('black background')
		for i in range(10, 0, -1):
			s.changePosition(0, 4)
			s.writeLine('Starting in {} '.format(i))
			time.sleep(1)

		s.clearScreen()
		p = 0
		for i in range(255):
			s.changePosition(0, p)
			s.setForeColor(i)
			now = datetime.now().strftime(timeFormat)
			s.writeLine(now + ' color = {}'.format(i))
			if p <= 8: p += 1
			else: p = 0
			time.sleep(2)

		s.clearScreen()
		p = 0
		for key, value in namedColors.items():
			s.changePosition(0, p)
			s.setForeColor(key)
			s.writeLine('Using Color {}'.format(key.title()))
			if p <= 8: p += 1
			else: p = 0
			time.sleep(2)

except KeyboardInterrupt:
	# exits when you press CTRL+C
	print('\nKeyBoard Interrupt')


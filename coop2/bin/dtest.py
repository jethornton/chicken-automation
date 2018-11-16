#!/usr/bin/env python3

from digole import lcd
import time
from datetime import datetime

timeFormat = '%I:%M %p'

s = lcd()

while True:
	s.clearScreen()
	for i in range(255):
		s.changePosition(0, 2)
		s.setForeColor(i)
		now = datetime.now().strftime(timeFormat)
		s.writeLine(now + ' color = {}'.format(i))
		time.sleep(2)


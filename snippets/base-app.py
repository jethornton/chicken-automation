#!/usr/bin/python3

'''
This is a basic framework to have an event timer so you can time out a
process like door opening.


This shows how to get a clean exit when killing your program with Ctrl c
'''

import sys, signal
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QTimer
import RPi.GPIO as GPIO

# setup I/O
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Chick(QCoreApplication):
	def __init__(self, *args, **kwargs):
		super(Chick, self).__init__(*args, **kwargs)
		# catch Ctrl C when ran from the terminal
		signal.signal(signal.SIGINT, self.cleanExit)
		updateTimer = QTimer(self)
		updateTimer.timeout.connect(self.run)
		updateTimer.start(1000)
		self.say = ''

	def run(self):
		if self.say == 'Tick':
			self.say = 'Tock'
		else:
			self.say = 'Tick'
		print(self.say)


	def cleanExit(self, signum, frame):
		GPIO.cleanup()
		print('\nCtrl C Pressed to Exit!')
		print('signum {} frame {}'.format(signum, frame))
		print('Clean Exit')
		sys.exit()

app = Chick(sys.argv)
app.exec_()


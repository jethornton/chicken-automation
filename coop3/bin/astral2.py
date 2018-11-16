#!/usr/bin/python3

import sys, os
from PyQt4 import QtGui, uic



class MyWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		path, filename = os.path.split(os.path.realpath(__file__))
		uic.loadUi(os.path.join(path, 'astral.ui'), self)
		self.connections()
		self.show()

	def connections(self):
		self.actionQuit.triggered.connect(sys.exit)
		self.updateAstral.clicked.connect(self.test)

	def test(self):
		print('testing')

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MyWindow()
	sys.exit(app.exec_())

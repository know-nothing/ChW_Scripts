# coding=utf-8

from os import environ, path
from time import ctime


class Logger:
	def __init__(self, filename='custom.log'):
		self.filename = path.join(environ['HOME'], filename)


	def log(self, msg):
		with open(self.filename, 'a') as file:
			print >> file, ctime(), ' -- ', msg.encode('utf8'), '\n'
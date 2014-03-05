'''
KTN-project 2013 / 2014
Python daemon thread class for listening for events on
a socket and notifying a listener of new messages or
if the connection breaks.

A python thread object is started by calling the start()
method on the class. in order to make the thread do any
useful work, you have to override the run() method from
the Thread superclass. NB! DO NOT call the run() method
directly, this will cause the thread to block and suspend the
entire calling process' stack until the run() is finished.
it is the start() method that is responsible for actually
executing the run() method in a new thread.
'''
from threading import Thread
import datetime
import Queue
from GlobalVar import *
import json
import re
class ReceiveMessageWorker(Thread):

	def __init__(self, connection, id):
		super(ReceiveMessageWorker, self).__init__()
		self.daemeon = True
		self.socket = connection
		self.id = id
		self.shutdown = False
                self.controlQueue = Queue.Queue()
	def run(self):
		while not self.shutdown:
			message = self.socket.recv(4096)
			print "DEUBG: message: " + str(message)
			data = json.loads(message)
			if data['request'] == 'login':
				print data['username'], userList;
				if unicode(data['username']) in userList.values():
					self.controlQueue.put((self.id, 'taken' + data['username']))
				else:
					if not data['username'].isalnum():
						self.controlQueue.put((self.id, 'invalid' + data['username']))
					else:
						userList[self.id] = data['username']
						self.controlQueue.put((self.id, 'login' + data['username']))
			elif data['request'] == 'logout':
				self.controlQueue.put((self.id, 'logout'))
                                return
			else:
				mtx.acquire()
				messageLog.append(unicode(datetime.datetime.today().time())[0:8] + " " + userList[self.id] + ': ' + unicode(data['message']))
				mtx.release()

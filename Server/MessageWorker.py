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
import json


class ReceiveMessageWorker(Thread):

    def __init__(self, listener, connection, id):
        self.daemeon = True
		self.socket = connection
		self.owner = listener
		self.id = id

    def run(self):
		while True:
			message = socket.recv(4096)
			data = json.loads(message)
			with mtx:
				if data['request'] == 'login':
					if data['username'] in userList.items():
						controlQueue.put((self.id, 'Invalid username' + data['username']))
					else:
						userList[self.id] = data['username']
						controlQueue.put((self.id, 'login'))
				else if data['request'] == 'logout':
					controlQueue.put((self.id, 'logout'))
				else:
					messageLog.append(self.username + ': ' + data['message'])
				

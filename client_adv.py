# -*- coding: utf-8 -*-
import socket
import json
from threading import Thread
class Client(object):
	Login = False
	def __init__(self):
		# Initialiser en tilkobling
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def listen(self):
		while True:
			recived_data = self.connection.recv(1024)
			data = json.loads(recived_data)
			if data['response']=='login' and data['error']=='Invalid username!':
				print data['response']+": "+data['error']+": "+data['username']+"\n"
				username = raw_input('Enter your username: ')
				request = 'login'
				self.send(json.dumps({'username':username,'request':request}))
			elif data['response']=='login' and data['error']=='Name already taken!':
				print data['response']+": "+data['error']+": "+data['username']+"\n"
				username = raw_input('Enter your username: ')
				request = 'login'
				self.send(json.dumps({'username':username,'request':request}))
			elif data['response']=='login':
				print data['response']+": "+data['username']+"\n"
				self.Login = True
			elif data['response']=='message' and data['error']=='You are not logged in!':
				username = raw_input('Enter your username: ')
				request = 'login'
				self.send(json.dumps({'username':username,'request':request}))
			elif data['response']=='message':
				print data['message']
			#print '\n'+ recived_data['response']
	def start(self, host, port):
		# Start tilkoblingen
		self.connection.connect((host, port))
		listen_thr = Thread(target = self.listen)
		listen_thr.start()
		# Be brukeren om å skrive inn brukernavn
		username = raw_input('Enter your username: ')
		request = 'login'
		self.send(json.dumps({'username':username,'request':request}))
		while self.Login == False:
			continue
		message = ''
		print('Enter a message (type "exit" to quit): ')
		while True:
			
			message = raw_input()

			# Lukk tilkoblingen hvis brukeren skriver "exit"
			if message == 'exit':
				self.send(json.dumps({'nick': nick, 'message': 'I\'m leaving. Goodbye!'}))
				self.connection.close()
				break
			# Konstruer et JSON objekt som som skal
			# sendes til serveren
			request='message'
			data = {'request':request , 'message': message}
			# Lag en streng av JSON-objektet
			data = json.dumps(data)
			# Send meldingen til serveren
			self.send(data)
			# Lag en metode for å sende en melding til serveren
	def send(self, data):
		self.connection.send(data)


# Kjøres når programmet startes
if __name__ == "__main__":
	# Definer host og port for serveren
	#HOST = 'localhost'
	#PORT = 9999
	HOST = raw_input('Enter hostname or ip address: ')
	PORT = input('Enter port: ')
	# Initialiser klienten
	client = Client()
	# Start klienten
	client.start(HOST, PORT)

#!/usr/bin/python2
'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''
import sys
import SocketServer
import thread
import mutex
from time import sleep
from GlobalVar import *
import MessageWorker
import uuid
from json import JSONEncoder
'''
The RequestHandler class for our server.

It is instantiated once per connection to the server, and must
overrid the handle() method to implement communication to the
client.
'''
class CLientHandler(SocketServer.BaseRequestHandler):
    def shutDown(self, reciever):
        reciever.shutdown = True
        reciever.join()
        print 'Client disconnected'
        self.exit()

    def printDebug(self, string):
        print "DEBUG: " + str(string)

    def sendError(self, error, username):
        data = JSONEncoder().encode({'response': 'login', 'error': error, 'username': username})
        print "Sending: " + str(data)
        self.connection.sendall(data)

    def sendResponse(self, response, username=None):
        if username:
            data = JSONEncoder().encode({'response': response, 'username': username})
        else:
            data = JSONEncoder().encode({'response': response})
        self.connection.sendall(data)

    def handle(self):
        # Get a reference to the socket object
        self.connection = self.request
        # Get the remote ip adress of the socket
        self.ip = self.client_address[0]
        # Get the remote port number of the socket
        self.port = self.client_address[1]
        self.id = uuid.uuid1()
        print 'Client connected @' + self.ip + ':' + str(self.port)
        print 'self.connection:' + str(self.connection) + '\n'
        print 'self.id:' + str(self.id) + '\n'
        reciever = MessageWorker.ReceiveMessageWorker(self.connection, self.id)
        reciever.start()

# Check for corret login
        controlObj = controlQueue.get(True)
        while controlObj[0] != self.id:
            controlQueue.put(controlObj)
            controlObj = controlQueue.pop()

        status = controlObj[1]
        if status[:7] == 'invalid':
            self.printDebug(status)
            self.sendError('Invalid username!', status[:7])
            self.shutDown(reciever)
        elif status[:5] == 'taken':
            self.printDebug(status)
            self.sendError('Name already taken!', status[5:])
            self.shutDown(reciever)
        elif status[:5] != 'login' or status == None:
            self.printDebug(status)
            self.sendError('Unknown error!', status)
            self.shutDown(reciever)
        else:
            self.printDebug(status)
            self.sendResponse('login', status[5:])

        msgNo = 0
        while True:
            mtx.acquire()
            while len(messageLog) > msgNo:
                self.connection.sendall(messageLog[msgNo])
                msgNo += 1
            mtx.release()

            controlObj = controlQueue.get()
            if controlObj[0] != self.id:
                controlQueue.put(controlObj)
            else:
                status = controlObj[1]
                if status[:5] == 'logout':
                    self.connection.sendall('logout\n' + status[6:])
                    printdebug(status)
                    self.shutDown(reciever)
            
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9998
    
    if (len(sys.argv) == 3):
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), CLientHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print "Starting server"
    server.serve_forever()

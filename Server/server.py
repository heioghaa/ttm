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
        print 'Shutting down'
        reciever.shutdown = True
        reciever.join()
        self.connection.close()
        print 'Client disconnected'

    def printDebug(self, string):
        print "DEBUG: " + str(string)

    def sendError(self, error, username):
        data = JSONEncoder().encode({'response': 'login', 'error': error, 'username': username})
        print "Sending: " + str(data)
        try:
            self.connection.sendall(data)
        except:
            self.shutdown()
            self.exit()

    def sendResponse(self, response, username=None):
        bla = 0
        data = ''
        if username:
            try:
                mtx.acquire()
                self.printDebug("CONNECTION!")
                if (len(messageLog) == 0):
                     data = JSONEncoder().encode({'response': response, 'username': username, 'messages': ''})
                else:
                    data = JSONEncoder().encode({'response': response, 'username': username, 'messages': messageLog[-10:-1]})
                    bla = len(messageLog)
            finally:
                mtx.release()
        else:
            data = JSONEncoder().encode({'response': response})

        self.printDebug(data)
        try:
            self.connection.sendall(data)
        except:
            self.printDebug("Broken pipe")
            self.shutDown()
            self.exit()

        return bla
            

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
        controlObj = reciever.controlQueue.get(True)
        if controlObj[0] != self.id:
        		printDebug("Something went horribly wrong")
        		exi()
        status = controlObj[1]
        if status[:7] == 'invalid':
            self.printDebug(status)
            self.sendError('Invalid username!', status[7:])
            self.shutDown(reciever)
            return
        elif status[:5] == 'taken':
            self.printDebug(status)
            self.sendError('Name already taken!', status[5:])
            self.shutDown(reciever)
            return
        elif status[:5] != 'login' or status == None:
            self.printDebug(status)
            self.sendError('Unknown error!', status)
            self.shutDown(reciever)
            return
        else:
            self.printDebug(status)
            msgNo = self.sendResponse('login', status[5:])

        while True:
            sleep(0.002)
            if not reciever.controlQueue.empty():
                controlObj = reciever.controlQueue.get_nowait()
                if controlObj[0] != self.id:
                   self.printDebug("Something went horribly wrong") 
                else:
                    status = controlObj[1]
                    self.printDebug(status)
                    if status[:6] == 'logout':
                        data = JSONEncoder().encode({'response': 'logout','username':status[6:]})
                        print data
                        try:
                            self.connection.sendall(data)
                        finally:
                            self.shutDown(reciever)
                            return
                    elif status == 'connerr':
                        self.shutDown(reciever)
                        return
            try:
                mtx.acquire()
                while len(messageLog) > msgNo:
                    data = JSONEncoder().encode({'response': 'message','message': messageLog[msgNo]})
                    try:
                        self.connection.sendall(data)
                    except:
                        self.printDebug("Broken pipe")
                        self.shutDown(reciever)
                        return
                    msgNo += 1
            finally:
                mtx.release()


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

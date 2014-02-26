#!/usr/bin/python2
'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''
import SocketServer
import thread
from time import sleep
import GlobalVar
import MessageWorker
import uuid
'''
The RequestHandler class for our server.

It is instantiated once per connection to the server, and must
overrid the handle() method to implement communication to the
client.
'''
class CLientHandler(SocketServer.BaseRequestHandler):
    def shutDown(self):
        reciever.shutdown = True
        reciever.join()
        print 'Client disconnected'
        self.exit()

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

        controlObj = GlobalVar.controlQueue.get(True)
        while controlObj[0] != self.id:
            controlQueue.put(controlObj)
            controlObj = controlQueue.pop()

        status = controlObj[1]
        if status[:15] == 'Invalid username':
            self.connection.sendall('login\n' + status[:15] + '\n' + status[16:])
            print status
            self.shutDown()
        elif status[:21] == 'Username already taken':
            self.connection.sendall('login\n' + status[22:] + '\n' + status[:21])
            print status
            self.shutDown()
        elif status[:4] != 'login':
            self.connection.sendall('login\nUnknown Error' + status[5:])
            print status
            self.shutDown()

        self.connection.sendall('login\n' + status[5:])
        print status
        msgNo = 0
        while True:
            while len(messageLog) >= msgNo:
                self.connection.sendall(messageLog[msgNo])
                msgNo += 1
            if controlQueue[0][0] == self.id:
                status = controlQueue.get()[1]
                if status[:5] == 'logout':
                    self.connection.sendall('logout\n' + status[6:])
                    print status
                    self.shutDown()
            
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9998

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), CLientHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print "Starting server"
    server.serve_forever()

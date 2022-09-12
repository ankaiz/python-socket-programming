"""
#import socket module
from socket import *
import sys # In order to terminate the program
import threading

##
class ClientThread(threading.Thread):
    def __init__(self,connect,addr):
        threading.Thread.__init__(self)
        self.connectionSocket = connect
        self.addr = addr
        global count
        count += 1
    def run(self):
        while True:
            try:
                print("count: %d"%count)
                message = self.connectionSocket.recv(1024)
                filename = message.split()[1]
                f = open(filename[1:])
                outputdata = f.read()
                print("[Debug] outputdata: %s"%(outputdata))
                #Send one HTTP header line into socket
                self.connectionSocket.send('HTTP/1.1 200 OK\n\n'.encode())
                #Send the content of the requested file to the client
                for i in range(0, len(outputdata)):
                    self.connectionSocket.send(outputdata[i].encode())
                self.connectionSocket.send("\r\n".encode())

                #self.connectionSocket.close()
            except IOError:
                #Send response message for file not found
                self.connectionSocket.send('HTTP/1.1 404 Not Found\n\n'.encode())
                self.connectionSocket.send('404 Not Found\n\n'.encode())
                #Close client socket
##

if __name__ == '__main__':

    serverSocket = socket(AF_INET, SOCK_STREAM)
    #Prepare a sever socket
    #Fill in start
    serverPort = 6789
    serverSocket.bind(('', serverPort))
    serverSocket.listen(3)
    threads=[]
    count = 0
    #Fill in end

    while True:
        #Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        client_socket = ClientThread(connectionSocket,addr)
        client_socket.setDaemon(True)
        client_socket.start()
        threads.append(client_socket)
        
    serverSocket.close()
"""

#改为Python3格式
#import socket module
from socket import *
import threading
def webProcess(connectionSocket):
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:], "rb")
        outputdata = f.read()
        outputdata = outputdata.decode()
        f.close()
        #Send one HTTP header line into socket
        outputdata = 'HTTP/1.1 200 OK\r\n\r\n' + outputdata
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
        print("OK!")
    except IOError:
        #Send response message for file not found
        outputdata = 'HTTP/1.1 404 Not Found\r\n\r\n'
        #Close client socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverPort = 6789
serverSocket.bind(("", serverPort))
serverSocket.listen(3)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    thread = threading.Thread(target = webProcess, args = (connectionSocket, ))
    thread.start()
serverSocket.close()
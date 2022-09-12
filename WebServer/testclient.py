#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
serverPort = 6789
serverSocket.connect(('', serverPort))
#Fill in end
print(serverSocket.recv(1024))
serverSocket.close()
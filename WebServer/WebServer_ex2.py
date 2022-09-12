#import socket module
from socket import *
import sys # In order to terminate the program


ip = sys.argv[1]
port = int(sys.argv[2])
filename = sys.argv[3]
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
serverSocket.connect((ip, port))
#Fill in end
#port = str(port)
message = "GET /%s HTTP/1.1\r\nHost: %s:%s\r\n\r\n"%(filename,ip,port)
serverSocket.send(message.encode())

print(serverSocket.recv(1024).decode())
serverSocket.close()
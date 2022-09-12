#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
#Fill in end
while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()#Fill in start              #Fill in end
    connectionSocket.send("THX conn".encode())
    message = connectionSocket.recv(1024)#Fill in start          #Fill in end
    print("[Debug] message:",message)
    connectionSocket.close()

sys.exit()#Terminate the program after sending the corresponding data
from socket import *
import sys
import os

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)
	
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
print("sys.argv[1]:",sys.argv[1])
serverip = sys.argv[1].split(':')[0]
serverport = int(sys.argv[1].split(':')[1].split('/')[0])
filename = sys.argv[1].split('/')[1]
print("serverip:",serverip)
print("serverport:",serverport)
print("filename:",filename)
tcpSerSock.bind((serverip, serverport))
tcpSerSock.listen(10)
# Fill in end.

while 1:
	# Strat receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
	message = tcpCliSock.recv(1024).decode()# Fill in start.		# Fill in end.
	#print("message:",message)
	# Extract the filename from the given message
	print("[Debug] message: ",message.split()[1])
	filename = message.split()[1].partition("/")[2]
	print("[filename]",filename)
	fileExist = "false"
	filetouse = "/" + filename
	print("[filetouse] ",filetouse)
	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "rb")
		outputdata = f.read()
		f.close()
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
		tcpCliSock.send("Content-Type:text/html\r\n".encode())
		# Fill in start.
		tcpCliSock.send(outputdata)
		# Fill in end.
		print('Read from cache')
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false":
			print("[Debug] if fileExist == false")
			# Create a socket on the proxyserver
			c = socket(AF_INET, SOCK_STREAM)# Fill in start.		# Fill in end.
			hostn = filename.replace("www.","",1)
			print("[hostn]",hostn)
			try:
				# Connect to the socket to port 80
				# Fill in start.
				ProxyServerName = hostn.partition("/")[0]
				ProxyServerPort = 80
				c.connect((ProxyServerName, ProxyServerPort))
				print("[ProxyServerName]",ProxyServerName)
				print("[ProxyServerPort]",ProxyServerPort)
				# Fill in end.
				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				print("[Debug] 1")
				fileobj = c.makefile('rwb', 0)
				print("[Debug] 2")
				msg = "GET http://" + filename + " HTTP/1.1\r\nHost: %s:%s\r\n\r\n"%(ProxyServerName,ProxyServerPort)
				print("[Debug] msg: ",msg)
				fileobj.write(msg.encode())
				#fileobj.write("GET ".encode() + "http://".encode() + filename.encode() + " HTTP/1.1\r\n".encode())
				#fileobj.write("GET ".encode() + askFile.encode() + " HTTP/1.0\r\nHost: ".encode() + serverName.encode() + "\r\n\r\n".encode())
				print("[Debug] 3")
				# Read the response into buffer
				# Fill in start.
				serverResponse = fileobj.read()
				print("[serverResponse_fileobj.read]",serverResponse.decode())
                # Fill in end.
				# Create a new file in the cache for the requested file. 
				# Also send the response in the buffer to client socket and the corresponding file in the cache
				tmpFile = open("./" + filename,"wb")  
				# Fill in start.
				serverResponse = serverResponse.split(b'\r\n\r\n')[1]
				print("[serverResponse_serverResponse.split]",serverResponse)
				tmpFile.write(serverResponse)
				tmpFile.close()
				tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
				tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
				tcpCliSock.send(serverResponse)
				# Fill in end.			
			except:
				print("Illegal request")                                               
		else:
			# HTTP response message for file not found
			# Fill in start.
			print("NET ERROR")
			# Fill in end.
	# Close the client and the server sockets    
	tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
# Fill in end.

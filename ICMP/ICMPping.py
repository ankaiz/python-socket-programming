from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

#original checksum function that calculate checksum through 'string'
def checksum_str(string): 
	print("[Debug] checksum_str")
	csum = 0
	countTo = (len(string) // 2) * 2  
	count = 0

	while count < countTo:
		thisVal = ord(string[count+1]) * 256 + ord(string[count])
		#print("[Debug] thisVal: ",thisVal)
		csum = csum + thisVal 
		csum = csum & 0xffffffff  
		count = count + 2
	
	if countTo < len(string):
		csum = csum + ord(string[len(string) - 1])
		csum = csum & 0xffffffff 
	
	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum 
	answer = answer & 0xffff 
	answer = answer >> 8 | (answer << 8 & 0xff00)
	print("[Debug] answer_str: ",answer)
	return answer

#modified checksum function that calculate through 'number'
def checksum(string): 
	print("[Debug] checksum")
	csum = 0
	countTo = (len(string) / 2) * 2  
	count = 0

	while count < countTo:
		thisVal = string[count+1] * 256 + string[count]
		#print("[Debug] thisVal: ",thisVal)
		csum = csum + thisVal 
		csum = csum & 0xffffffff  
		count = count + 2
	
	if countTo < len(string):
		csum = csum + string[len(string) - 1]
		csum = csum & 0xffffffff 
	
	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum 
	answer = answer & 0xffff 
	answer = answer >> 8 | (answer << 8 & 0xff00)
	print("[Debug] answer: ",answer)
	return answer
	
def receiveOnePing(mySocket, ID, timeout, destAddr):
	timeLeft = timeout
	print("[Debug] receiveOnePing")
	while 1: 
		startedSelect = time.time()
		whatReady = select.select([mySocket], [], [], timeLeft)
		howLongInSelect = (time.time() - startedSelect)
		if whatReady[0] == []: # Timeout
			print("[Debug] if whatReady[0] == []")
			return "Request timed out."
	
		timeReceived = time.time() 
		recPacket, addr = mySocket.recvfrom(1024)
	       
		#Fill in start
        
		#Fetch the ICMP header from the IP packet
		print("[Debug] recPacket: %s"%(recPacket))
		icmph = recPacket[20:28]
		print("[Debug] icmph: %s"%(icmph))
		type, code, checksum, pID, sq = struct.unpack("bbHHh", icmph)
		
		print("The header received in the ICMP reply is ",type, code, checksum, pID, sq)
		if pID == ID:
		    bytesinDbl = struct.calcsize("d")
		    timeSent = struct.unpack("d", recPacket[28:28 + bytesinDbl])[0]
		    rtt=timeReceived - timeSent
		    print("RTT is :",rtt)
		    return rtt
       	#Fill in end
		timeLeft = timeLeft - howLongInSelect
		if timeLeft <= 0:
			print("[Debug] if timeLeft <= 0")
			return "Request timed out."
	
def sendOnePing(mySocket, destAddr, ID):
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)
	print("[Debug] sendOnePing")
	myChecksum = 0
	myChecksum_str = 0
	# Make a dummy header with a 0 checksum
	# struct -- Interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	# Calculate the checksum on the data and the dummy header.
	myChecksum = checksum(header + data)
	myChecksum_str  = checksum_str(str(header + data))
	
	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
		# Convert 16-bit integers from host to network  byte order
		myChecksum = htons(myChecksum) & 0xffff		
	else:
		myChecksum = htons(myChecksum)
		
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data
	print("[Debug] packet:",packet)
	print("[Debug] packet_len:",len(packet))
	mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.
	
def doOnePing(destAddr, timeout): 
	icmp = getprotobyname("icmp")
	# SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw
	print("[Debug] icmp:",icmp)
	mySocket = socket(AF_INET, SOCK_RAW, icmp)
	
	myID = os.getpid() & 0xFFFF  # Return the current process i
	sendOnePing(mySocket, destAddr, myID)
	delay = receiveOnePing(mySocket, myID, timeout, destAddr)
	
	mySocket.close()
	return delay
	
def ping(host, timeout=1):
	# timeout=1 means: If one second goes by without a reply from the server,
	# the client assumes that either the client's ping or the server's pong is lost
	dest = gethostbyname(host)
	print("Pinging " + dest + " using Python:")
	# Send ping requests to a server separated by approximately one second
	while 1 :
		delay = doOnePing(dest, timeout)
		print(delay)
		time.sleep(1)# one second
	return delay
	
#ping("127.0.0.1")
destServer = "google.com"
ping(destServer)
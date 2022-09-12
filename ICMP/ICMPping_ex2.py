from socket import *
import os
import sys
import struct
import time
import select
import binascii  

ICMP_ECHO_REQUEST = 8

def checksum(string): 
	csum = 0
	countTo = (len(string) / 2) * 2  
	count = 0

	while count < countTo:
		thisVal = string[count+1] * 256 + string[count]
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
	return answer
	
def receiveOnePing(mySocket, ID, timeout, destAddr):
	timeLeft = timeout
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
		icmph = recPacket[20:28]
		type, code, checksum, pID, sq = struct.unpack("bbHHh", icmph)
		
		print("The header received in the ICMP reply is ",type, code, checksum, pID, sq)

		if(type != 0 or code != 0 or pID != ID or sq != 1):
			if (type == 3):
				if (code == 0):
					return "Network Unreachable"
				elif (code == 1):
					return "Host Unreachable"
				elif (code == 2):
					return "Protocol Unreachable"
				elif (code == 3):
					return "Port Unreachable"
				elif (code == 4):
					return "Fragmentation Needed and DF set"
				elif (code == 5):
					return "Source Route Failed"
				elif (code == 6):
					return "Destination Network Unknown"
				elif (code == 7):
					return "Destination Host Unknown"
				elif (code == 8):
					return "Source Host Isolated"
				elif (code == 9):
					return "Communication with Destination Network Administratively Prohibited"
				elif (code == 10):
					return "Communication with Destination Host Administratively Prohibited"
				elif (code == 11):
					return "Network Unreachable for Type of Service"
				elif (code == 12):
					return "Host Unreachable for Type of Service"
				else:
					return "Type is 3 , other error"
			elif (type == 4):
				return "Source Quench"
			elif (type == 5):
				if (code == 0):
					return "Redirect Datagram for the Net"
				elif (code == 1):
					return "Redirect Datagram for the Host"
				elif (code == 2):
					return "Redirect Datagram for the Type of Service and Net"
				elif (code == 3):
					return "Redirect Datagram for the Type of Service and Host"
			
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
	
	myChecksum = 0
	# Make a dummy header with a 0 checksum
	# struct -- Interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	# Calculate the checksum on the data and the dummy header.
	myChecksum = checksum(header + data)
	
	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
		# Convert 16-bit integers from host to network  byte order
		myChecksum = htons(myChecksum) & 0xffff		
	else:
		myChecksum = htons(myChecksum)
		
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data
	
	mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.
	
def doOnePing(destAddr, timeout): 
	icmp = getprotobyname("icmp")
	# SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw

	mySocket = socket(AF_INET, SOCK_RAW, icmp)
	
	myID = os.getpid() & 0xFFFF  # Return the current process i
	sendOnePing(mySocket, destAddr, myID)
	delay = receiveOnePing(mySocket, myID, timeout, destAddr)
	
	mySocket.close()
	return delay
	
def ping(host, timeout=1):
	delayList = []
	loopnum = 3
	avgrtt = 0.0
	lost = 0
	# timeout=1 means: If one second goes by without a reply from the server,
	# the client assumes that either the client's ping or the server's pong is lost
	dest = gethostbyname(host)
	print("Pinging " + dest + " using Python:")
	print("")
	# Send ping requests to a server separated by approximately one second
	for i in range(0,loopnum):
	#while 1 :
		print("Loop: %d"%i)
		delay = doOnePing(dest, timeout)
		if type(delay) == str:
			lost += 1
		else:
			delayList.append(delay)
			avgrtt += delay
		print("delay: ",delay)
		time.sleep(1)# one second
	if delayList :
		print("Max delay: ",max(delayList))
		print("Min delay: ",min(delayList))
		print("Avg delay: ",float(avgrtt/loopnum))
	print("Lost: ",lost,"Lost rate: %d%%" %((lost/loopnum)*100))
	#return delay


#ping("140.123.90.53")
#ping("127.0.0.1")
ping("google.com")

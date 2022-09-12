from socket import *
import os
import sys
import struct
import time
import select
import binascii  
		
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT  = 2.0 
TRIES    = 2
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise
def checksum(string): 
# In this function we make the checksum of our packet
# hint: see icmpPing lab
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
	return answer
def build_packet():
# In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
# packet to be sent was made, secondly the checksum was appended to the header and
# then finally the complete packet was sent to the destination.

# Make the header in a similar way to the ping exercise.
# Append checksum to the header.
	myChecksum = 0
	ID = os.getpid() & 0xFFFF  # Return the current process i
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	# Get the right checksum, and put in the header
	myChecksum = checksum(header + data)
	if sys.platform == 'darwin':
	# Convert 16-bit integers from host to network  byte order
		myChecksum = htons(myChecksum) & 0xffff		
	else:
		myChecksum = htons(myChecksum)
	
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
# Don’t send the packet yet , just return the final packet in this function.

# So the function ending should look like this

	packet = header + data
	return packet 

def dns_ptr_lookup(addr):
		try:
			return gethostbyaddr(addr)[0]
		except herror:
			return None

def get_route(hostname):
	timeLeft = TIMEOUT
	for ttl in range(1,MAX_HOPS):
		for tries in range(TRIES):
			destAddr = gethostbyname(hostname)
			
			#Fill in start
			# Make a raw socket named mySocket
			icmp = getprotobyname("icmp")
			mySocket = socket(AF_INET, SOCK_RAW, icmp)
            #Fill in end 
			mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
			mySocket.settimeout(TIMEOUT)
			try:
				d = build_packet()
				mySocket.sendto(d, (hostname, 0))
				t= time.time()
				startedSelect = time.time()
				whatReady = select.select([mySocket], [], [], timeLeft)
				howLongInSelect = (time.time() - startedSelect)
				if whatReady[0] == []: # Timeout
					print("  *        *        *    Request timed out.")
				recvPacket, addr = mySocket.recvfrom(1024)
				routehostname = dns_ptr_lookup(addr[0])
				timeReceived = time.time()
				timeLeft = timeLeft - howLongInSelect
				if timeLeft <= 0:
					print("  *        *        *    Request timed out.")

			except timeout:
				continue			
			
			else:
				#Fill in start        
        		#Fetch the icmp type from the IP packet 
				icmph = recvPacket[20:28]
				types, code, checksum, pID, sq = struct.unpack("bbHHh", icmph)
        		#Fill in end
				
				if types == 11:
					bytes = struct.calcsize("d") 
					timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
					print("%d    rtt=%.0f ms    routeaddr %s, routename %s" %(ttl, (timeReceived -t)*1000, addr[0],routehostname))
				
				elif types == 3:
					bytes = struct.calcsize("d") 
					timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
					print("%d    rtt=%.0f ms    routeaddr %s, routename %s" %(ttl, (timeReceived-t)*1000, addr[0],routehostname))
				
				elif types == 0:
					bytes = struct.calcsize("d") 
					timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
					print("%d    rtt=%.0f ms    routeaddr %s, routename %s" %(ttl, (timeReceived - timeSent)*1000, addr[0],routehostname))
					return
			
				else:
					print("error")			
				break	
			finally:				
				mySocket.close()		

print("google.com")
get_route("google.com")
print("ccu.edu.tw")
get_route("ccu.edu.tw")
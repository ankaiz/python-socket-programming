# UDPPingerClient.py
from socket import *
import time

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
addr = ("127.0.0.1", 12000)
message = "ping"

for i in range(10):
    start_time = time.time()
    clientSocket.sendto(message.encode(), addr)
    try:
        res_message, addr = clientSocket.recvfrom(1024)
        end_time = time.time()
        RTT = end_time - start_time
        print("LOOP: %d"%i)
        print("res_message: %s"%res_message)
        print("RTT: %fs"%RTT)
    except timeout: #??
        print("[Debug] clientSocket.timeout",clientSocket.timeout)
        print("LOOP: %d"%i)
        print("Timeedout")
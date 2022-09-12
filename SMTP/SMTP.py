
from socket import *

msg = "\r\n I love computer networks!\r\n"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("outgoing.ccu.edu.tw",25)
# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start  
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
#Fill in end
recv = clientSocket.recv(1024).decode()
print("recv:" +recv)
if recv[:3] != '220':
	print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print("recv1: "+recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
# Fill in start
mailFrom = "MAIL FROM: <g11430039@ccu.edu.tw> \r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024).decode()
print("After MAIL FROM command: "+recv2)
if recv1[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send RCPT TO command and print server response. 
# Fill in start
rcptTo = "RCPT TO: <g11430039@ccu.edu.tw> \r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024).decode()
print("After RCPT TO command: "+recv3)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Fill in end

# Send DATA command and print server response. 
# Fill in start
data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024).decode()
print("After DATA command: "+recv4)
if recv1[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send message data.
# Fill in start
subject = "Subject: SMTP mail client testing\r\n\r\n"
clientSocket.send(subject.encode())
clientSocket.send(msg.encode())
# Fill in end

# Message ends with a single period.
# Fill in start
clientSocket.send(endmsg.encode())
# Fill in end

recv_msg = clientSocket.recv(1024).decode()
print("Response after sending message body:"+recv_msg)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
# Fill in start
clientSocket.send("QUIT\r\n".encode())
message=clientSocket.recv(1024).decode()
print (message)
clientSocket.close()
# Fill in end

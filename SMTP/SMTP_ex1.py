
from socket import *
import base64
import ssl
msg = "\r\n I love computer networks!\r\n\r\n"
endmsg = "\r\n.\r\n"
username = "iio051611"
password = "cdwpngpofwqengcs"

# Choose a mail server (e.g. Google mail server) and call it mailserver
#mailserver = ("127.0.0.1", 25)#Fill in start   #Fill in end
#mailserver = ("outgoing.ccu.edu.tw",25)
hostname = "smtp.gmail.com"
mailserver = (hostname,465)
#mailserver = ("smtp.office365.com",587)
# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start  
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
context = ssl.create_default_context()
clientSocketSSL = context.wrap_socket(clientSocket, server_hostname=hostname)
#Fill in end
recv = clientSocketSSL.recv(1024).decode()
print("recv:" +recv)
if recv[:3] != '220':
	print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocketSSL.send(heloCommand.encode())
recv1 = clientSocketSSL.recv(1024).decode()
print("recv1: "+recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

#Info for username and password
loginCommand = 'auth login\r\n'
while True:
    clientSocketSSL.send(loginCommand.encode())
    recv = clientSocketSSL.recv(1024)
    recv = recv.decode()
    print(recv)
    if recv[:3] == '334':
        break

userCommand = base64.b64encode(username.encode()) + b'\r\n'
while True:
    clientSocketSSL.send(userCommand)
    recv = clientSocketSSL.recv(1024)
    recv = recv.decode()
    print(recv)
    if recv[:3] == '334':
        break

passCommand = base64.b64encode(password.encode()) + b'\r\n'
while True:
    clientSocketSSL.send(passCommand)
    recv = clientSocketSSL.recv(1024)
    recv = recv.decode()
    print(recv)
    if recv[:3] == '235':
        break

# Send MAIL FROM command and print server response.
# Fill in start
#mailFrom = "MAIL FROM: <g11430039@ccu.edu.tw> \r\n"
mailFrom = "MAIL FROM: <iio051611@gmail.com> \r\n"
clientSocketSSL.send(mailFrom.encode())
recv2 = clientSocketSSL.recv(1024).decode()
print("After MAIL FROM command: "+recv2)
if recv1[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send RCPT TO command and print server response. 
# Fill in start
#rcptTo = "RCPT TO: <g11430039@ccu.edu.tw> \r\n"
rcptTo = "RCPT TO: <iio051611@gmail.com> \r\n"
clientSocketSSL.send(rcptTo.encode())
recv3 = clientSocketSSL.recv(1024).decode()
print("After RCPT TO command: "+recv3)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Fill in end

# Send DATA command and print server response. 
# Fill in start
data = "DATA\r\n"
clientSocketSSL.send(data.encode())
recv4 = clientSocketSSL.recv(1024).decode()
print("After DATA command: "+recv4)
if recv1[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send message data.
# Fill in start
subject = "Subject: SMTP EX1 mail client testing\r\n\r\n"
clientSocketSSL.send(subject.encode())
clientSocketSSL.send(msg.encode())
# Fill in end

# Message ends with a single period.
# Fill in start
clientSocketSSL.send(endmsg.encode())
# Fill in end

recv_msg = clientSocketSSL.recv(1024).decode()
print("Response after sending message body:"+recv_msg)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
# Fill in start
clientSocketSSL.send("QUIT\r\n".encode())
message=clientSocketSSL.recv(1024).decode()
print (message)
clientSocketSSL.close()
# Fill in end


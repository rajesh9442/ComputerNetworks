import socket
import sys
import re

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))
 
port = 25

try:
    host_ip = socket.gethostbyname('mail.getnada.com')
    print("ip::",host_ip)
except socket.gaierror:
    print ("there was an error resolving the host")
    sys.exit()
mailserver=(host_ip, port)
s.connect(mailserver)
 
print ("the socket has successfully connected to getnada")
recv = s.recv(1024).decode()
print("Message after connection request:" + recv)
if recv[:3] != '220':
    print('220 reply not recieved from the server')
 
for item in range(1,len(sys.argv)):
    file=open(sys.argv[item],'r')
    senderid=file.readline()
    mailfr=str(re.findall(r'\<.*?\>',senderid))
    mailfrom=mailfr[2:len(mailfr)-2]
    print("mailll::",mailfrom)
    recipientid=file.readline().split()[2]
    rcptid=str(re.findall(r'\<.*?\>',recipientid))
    rcptto=rcptid[2:len(rcptid)-2]
    print("to::",rcptto)
    subject=file.readline()
    print("subject::",subject)
    file.readline()
    message=file.readline()
    print("message::",message)

    # Send HELO command and print server response.
    heloCommand = 'HELO Professor\r\n'
    new=s.send(heloCommand.encode())
    recv1 = s.recv(1024).decode()
    print("reciever:",new)
    if recv1[:3] != '250':
        print('250 reply not recieved from the server')

    # Mail From
    sender = "MAIL FROM:"+mailfrom+"\r\n"
    s.send(sender.encode())
    recv2 = s.recv(1024).decode()

    # Rcpt to
    reciever = "RCPT TO:"+rcptto+"\r\n"
    s.send(reciever.encode())
    recv3=s.recv(1024).decode

    # DATA command
    data = "DATA\r\n"
    s.send(data.encode())
    recv4 = s.recv(1024).decode()
    print("recv4:",recv4)

    # Message data
    subject = subject+"\r\n"
    s.send(subject.encode())
    msgData = message+"\r\n"
    s.send(msgData.encode())
    s.send(".\r\n".encode())
    recv5=s.recv(1024).decode()
    print("recv5",recv5)

# Send QUIT command and handle server response.
quit = "QUIT\r\n"
s.send(quit.encode())
recv6 = s.recv(1024).decode()
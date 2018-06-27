import socket
import encry
import os

TCP_IP = '0.0.0.0'
TCP_PORT = 5005
BUFFER_SIZE = 4096

"""conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.connect(("8.8.8.8", 80))
ip = (conn.getsockname()[0])
conn.close()

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(("", 5005))
conn.send(ip)
data = conn.recv(512)
conn.close()
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
mainc = 0
prev = []

data = conn.recv(BUFFER_SIZE)
conn.send(data)

f = open("public_key2.pem", "wb")
f.write(data)
f.close()

while 1:
    data = conn.recv(BUFFER_SIZE)
    f = open("eText.txt","wb")
    f.write(data)
    f.close()
    encry.writeDecrypt()
    f = open("dText.txt","rb")
    x = f.read()
    f.close()
    c = 0
    while 1:
    	if x[c] == "^" and x[c+1] == "$":
    		x = x[:c]
    		prev.append(x)
    		break
    	c+=1

    if not x:
    	mainc +=1
    	continue
    if mainc == 0:
    	print x
    elif prev[mainc-1] != x:
		print x

    mainc += 1

    if not data:
    	break
    conn.send(x)

conn.close()
#encry.cleanup()

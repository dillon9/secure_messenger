import socket
import encry
import os

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 512

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
while 1:
    data = conn.recv(BUFFER_SIZE)
    f = open("text.txt","wb")
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
    		print x
    		break
    	c+=1

    if not data: break
    conn.send(x)


conn.close()
#encry.cleanup()

#os.remove("private_key.pem")
#os.remove("public_key.pem")
#os.remove("eText.txt")
#os.remove("dText.txt")
#os.remove("text.txt")
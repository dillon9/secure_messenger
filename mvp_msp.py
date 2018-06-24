
import socket
import encry
import os
sendOn = "127.0.0.1"
sendPort = 5005

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((sendOn, sendPort))
encry.genKey()
while 1:
	f = open("text.txt","wb")
	f.write(raw_input()+"^$")
	f.close()
	
	encry.writeEncrpyt()

	f = open("eText.txt","rb")
	x = f.read()
	f.close()

	conn.send(x)
	data = conn.recv(1024)
conn.close()
#encry.cleanup()
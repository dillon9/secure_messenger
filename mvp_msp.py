
import socket


sendOn = "192.168.1.117"
sendPort = 5005
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((sendOn, sendPort))
while 1:
	conn.send(raw_input())
	data = conn.recv(512)
conn.close()

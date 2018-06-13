import socket


TCP_IP = '192.168.1.117'
TCP_PORT = 5005
BUFFER_SIZE = 512

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(2)

conn, addr = s.accept()
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print data
    conn.send(data)
conn.close()
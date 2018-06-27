import socket
import os
import thread
import time
import miniupnpc
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64
import os

#Enable this if upnp is enabled on your router
#otherwise manually forward the port
"""
port = 5005
proto = "TCP"
description = "Python p2p chat"

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 10
upnp.discover()
upnp.selectigd()

try:
	upnp.addportmapping(port, proto, upnp.lanaddr, port, description, '')
except Exception, e:
	print "Unable to add UPnP port mapping. ", e
"""

def genKey():
	new_key = RSA.generate(4096, e=65537)
	private_key = new_key.exportKey("PEM")
	public_key = new_key.publickey().exportKey("PEM")
	fd = open("private_key.pem", "wb")
	fd.write(private_key)
	fd.close()
	fd = open("public_key.pem", "wb")
	fd.write(public_key)
	fd.close()

def encrypt_blob(blob, public_key):
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    blob = zlib.compress(blob)
    chunk_size = 470
    offset = 0
    end_loop = False
    encrypted =  ""

    while not end_loop:
        chunk = blob[offset:offset + chunk_size]
        if len(chunk) % chunk_size != 0:
            end_loop = True
            chunk += " " * (chunk_size - len(chunk))
        encrypted += rsa_key.encrypt(chunk)
        offset += chunk_size
    return base64.b64encode(encrypted)

def writeEncrpyt():
	fd = open("peer_public.pem", "rb")
	public_key = fd.read()
	fd.close()

	fd = open("text.txt", "rb")
	unencrypted_blob = fd.read()
	fd.close()

	encrypted_blob = encrypt_blob(unencrypted_blob, public_key)

	fd = open("eText.txt", "wb")
	fd.write(encrypted_blob)
	fd.close()


def decrypt_blob(encrypted_blob, private_key):
    rsakey = RSA.importKey(private_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted_blob = base64.b64decode(encrypted_blob)
    chunk_size = 512
    offset = 0
    decrypted = ""
    while offset < len(encrypted_blob):
        chunk = encrypted_blob[offset: offset + chunk_size]
        decrypted += rsakey.decrypt(chunk)
        offset += chunk_size
    return zlib.decompress(decrypted)

def cleanup():
	os.remove("private_key.pem")
	os.remove("public_key.pem")
	os.remove("eText.txt")
	os.remove("dText.txt")
	os.remove("text.txt")

def writeDecrypt():
	fd = open("private_key.pem", "rb")
	private_key = fd.read()
	fd.close()

	fd = open("eText.txt", "rb")
	encrypted_blob = fd.read()
	fd.close()

	fd = open("dText.txt", "wb")
	fd.write(decrypt_blob(encrypted_blob, private_key))
	fd.close()


def client(unused, unused2):
	sendTo = "127.0.0.1"
	sendPort = 5005
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	conn.connect((sendTo, sendPort))
	genKey()

	f = open("public_key.pem", "rb")
	pubkey = f.read()
	conn.send(pubkey)
	f.close()

	while 1:
		f = open("text.txt","wb")
		writeTo = raw_input()
		if not writeTo:
			print "Enter something"
			f.close()
			continue
		f.write(writeTo+"^$")
		f.close()

		writeEncrpyt()

		f = open("eText.txt","rb")
		x = f.read()
		f.close()

		conn.send(x)
		data = conn.recv(1024)
	conn.close()

def server(unused, unused2):
	TCP_IP = '0.0.0.0'
	TCP_PORT = 5005
	BUFFER_SIZE = 4096

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	conn, addr = s.accept()
	mainc = 0
	prev = []

	data = conn.recv(BUFFER_SIZE)
	conn.send(data)

	f = open("peer_public.pem", "wb")
	f.write(data)
	f.close()

	while 1:
	    data = conn.recv(BUFFER_SIZE)
	    f = open("eText.txt","wb")
	    f.write(data)
	    f.close()
	    writeDecrypt()
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

#try:
thread.start_new_thread(server,("Server-Thread",5))
time.sleep(2)
thread.start_new_thread(client,("Client-Thread",5))
#except:
	#print "Of course it doesn't work the first time idiot"

while 1:
	pass
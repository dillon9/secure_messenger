from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64
import os

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
	fd = open("public_key2.pem", "rb")
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

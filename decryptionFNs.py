#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import sys
#from Crypto.Cipher import Blowfish
from base64 import b64encode, b64decode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import json
from Crypto.Cipher import Salsa20


def decrypt_file(username,file_name):
	schemeLines = [line.rstrip('\n') for line in open('scheme_'+username+'.txt')]
	scheme = schemeLines[0]
	with open('key_'+username+'.txt','rb') as fp:
		key = fp.read()

	if scheme == "AES":
		with open(file_name, 'rb') as fo:
			nonce, tag, ciphertext = [ fo.read(x) for x in (16,16,-1) ]
		cipher = AES.new(key,AES.MODE_EAX, nonce)
		data = cipher.decrypt_and_verify(ciphertext, tag)
		os.remove(file_name)
		with open(file_name,'wb') as g:
			g.write(data)

	if scheme == "ChaCha20":
		with open(file_name,'r') as f:
			json_input = f.read()
		b64 = json.loads(json_input)
		nonce = b64decode(b64['nonce'])
		ciphertext = b64decode(b64['ciphertext'])
		cipher = ChaCha20.new(key=key, nonce=nonce)
		plaintext = cipher.decrypt(ciphertext)
		os.remove(file_name)
		with open(file_name,'wb') as g:
			g.write(plaintext)

	if scheme == 'Salsa20':
		with open(file_name, 'rb') as fo:
			msg = fo.read()      
		msg_nonce = msg[:8]
		ciphertext = msg[8:]
		cipher = Salsa20.new(key=key, nonce=msg_nonce)
		plaintext = cipher.decrypt(ciphertext)
		os.remove(file_name)
		with open(file_name,'wb') as g:
			g.write(plaintext) 
#decrypt_file('check4','execution_times')
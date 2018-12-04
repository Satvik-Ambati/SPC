#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import sys
from Crypto.Cipher import Blowfish
from base64 import b64encode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import json
from Crypto.Cipher import Salsa20



def encrypt_file(username,file_name):

	schemeLines = [line.rstrip('\n') for line in open('scheme_'+username+'.txt')]
	scheme = schemeLines[0]
	with open('key_'+username+'.txt','rb') as fp:
		key = fp.read()
	if scheme == "AES":
		with open(file_name, 'rb') as fo:
			plaintext = fo.read()
		cipher = AES.new(key,AES.MODE_EAX)
		ciphertext, tag = cipher.encrypt_and_digest(plaintext)
		os.remove(file_name)
		with open(file_name , 'wb+') as fo:
			[ fo.write(x) for x in (cipher.nonce, tag, ciphertext) ]
	if scheme == "Salsa20":
		with open(file_name, 'rb') as fo:
			plaintext = fo.read()
		cipher = Salsa20.new(key=key)
		msg = cipher.nonce + cipher.encrypt(plaintext)
		os.remove(file_name)
		with open(file_name,'wb+') as g:
			g.write(msg)
	if scheme == "ChaCha20":
		cipher = ChaCha20.new(key=key)
		with open(file_name,'rb') as fo:
			plaintext = fo.read()
		ciphertext = cipher.encrypt(plaintext)
		nonce = b64encode(cipher.nonce).decode('utf-8')
		ct = b64encode(ciphertext).decode('utf-8')
		result = json.dumps({'nonce':nonce, 'ciphertext':ct})
		os.remove(file_name) 
		with open(file_name ,"w") as fo:
			fo.write(result)
#encrypt_file('check4','execution_times')
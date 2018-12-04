from Crypto import Random
import requests
import getpass
import re
import os
from Crypto.Cipher import AES
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
		with open(file_name ,"w+") as fo:
			fo.write(result)



if (os.stat("login_details.txt").st_size == 0):
	print("You need to login first")
	username = input('Username:')
	pswd = getpass.getpass('Password:')
	f=open("login_details.txt","w")
	f.write(username)
	f.write('\n'+pswd)
	f.close()
else:
	lines = [line.rstrip('\n') for line in open('login_details.txt')]
	username=lines[0]
	pswd=lines[1]

f=open('url.txt','r')
host = f.read()[:]
f.close()
	
url= 'http://'+host+'/account/login/'
session=requests.Session()
request = session.post(url, data = {'username':username , 'password':pswd})
res = request.text
ans = re.findall("(Secure Personal Cloud)",res)
if len(ans)==1:
	print("Successfully logged in")
	url1= 'http://'+host+'/account/upload/'
	directory = input('Directory or file path:')
	if os.path.isdir(directory):
		for (dirpath, dirnames, filenames) in os.walk(directory):
			for file in filenames:
				# relDir = os.path.relpath(dirpath, os.path.dirname(directory))
				file_path=os.path.join(dirpath,file)
				reldirname = directory.split('/')[-1]
				tempath = file_path.split('/'+reldirname+'/')[-1]
				
				if "/" in directory: 
					relfilepath = os.path.join(reldirname,tempath)
				else:
					relfilepath = tempath

				print("Uploading "+relfilepath)

				
				if os.path.isfile("scheme_"+username+".txt"):
					pass
				else:
					f = open("scheme_"+username+".txt","w+")
					f.write('AES')
					f.close()
				if os.path.isfile("key_"+username+".txt"):
					pass
				else:
					key = Random.get_random_bytes(32)
					f = open("key_"+username+".txt","wb+")
					f.write(key)
					f.close()

				with open(file_path,'rb') as f:
					x = f.read()
				encrypt_file(username,file_path)

				with open(file_path,'rb') as obj:
					files= {'document': obj}
					response=session.post(url1 , data = {'description':relfilepath}, files=files )
				os.remove(file_path)
				with open(file_path,'wb+') as f:
					f.write(x)	
	else:
		filename = directory.split('/')[-1]
		print("Uploading "+filename)


		if os.path.isfile("scheme_"+username+".txt"):
			pass
		else:
			f = open("scheme_"+username+".txt","w+")
			f.write('AES')
			f.close()
		if os.path.isfile("key_"+username+".txt"):
			pass
		else:
			key = Random.get_random_bytes(32)
			f = open("key_"+username+".txt","wb+")
			f.write(key)
			f.close()
		with open(directory,'rb') as f:
				x = f.read()
		encrypt_file(username,directory)

		with open(directory,'rb') as obj:
			files= {'document': obj}
			response=session.post(url1 , data = {'description':filename}, files=files )
		os.remove(directory)
		with open(directory,'wb+') as f:
			f.write(x)				
else:
	print("Invalid login credentials")
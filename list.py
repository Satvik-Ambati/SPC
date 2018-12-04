#!/u[:-1]sr/bin/python3

from Crypto import Random
import requests
import getpass
import re
import os

f=open('url.txt','r')
host = f.read()[:]
f.close()


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
	
url= 'http://'+host+'/account/login/'
session=requests.Session()
request = session.post(url, data = {'username':username , 'password':pswd})
res = request.text
ans = re.findall("(Secure Personal Cloud)",res)
if len(ans)==1:
	if os.path.isfile("scheme_"+username+".txt"):
		scheme = [line.rstrip('\n') for line in open('scheme_'+username+'.txt')][0]
		if scheme == 'AES':
			print('AES  <--  current en-de scheme')
			print('Salsa20')
			print('ChaCha20')
		elif scheme == 'Salsa20':
			print('AES')
			print('Salsa20  <--  current en-de scheme')
			print('ChaCha20')
		elif scheme == 'ChaCha20':
			print('AES')
			print('Salsa20')
			print('ChaCha20  <--  current en-de scheme')
		else:
			print('Not a valid encryption scheme')
else:
	print("Invalid login credentials")
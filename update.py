import requests
import getpass
import re
import os
import sys
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from base64 import b64encode, b64decode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import json
from os import listdir
from os.path import isfile, join
from Crypto.Cipher import Salsa20


f=open('url.txt','r')
host = f.read()[:]
f.close()

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
	print("Successfully logged in")

	#f = open("observe.txt",'r')
	#directory=f.read()


	url1='http://'+host+'/account/allfiles'
	request2 = session.get(url1)
	#print(request2)
	soup = BeautifulSoup(request2.text,'html.parser')
	files = soup.find(attrs={'class':'container'}).find_all('a',attrs={'class':'display_link'})
	fls=soup.find(attrs={'class':'container'}).find_all('a')
	#print((str(files[1]).split('<')[1]).split('>')[1])
	#print(len(files))
	newScheme = input('New En-De Scheme: ')

	#Lets deal with files first:
	for i in range(0,len(files)):
		#print(files[i])
		filename=(str(files[i]).split('<')[1]).split('>')[1]
		#print(filename)

		Href=files[i].get("href")
		p2=requests.get(urljoin('http://'+host, str(Href)))
		name=filename.replace('/','^')
		#print(name)

		with open(name,"wb") as t:
			t.write(p2.content)
		decrypt_file(username,name)

		
		
		if os.path.isfile("scheme_"+username+".txt"):
			sch = [line.rstrip('\n') for line in open('scheme_'+username+'.txt')]
			oldScheme=sch[0]
			if newScheme==oldScheme:
				for i in range(0,len(fls)):
					fn=(str(fls[i]).split('<')[1]).split('>')[1]
					#print(fn)
					if fn==filename:
						hreff=fls[i+2].get("href")	
						#print(hreff)		
						urldel='http://'+host+str(hreff)
						q=session.get(urldel)
						#print(q)

						encrypt_file(username,name)

						url2= 'http://'+host+'/account/upload/'
						with open(name,'rb') as obj:
							name2=name.replace('^','/')
							print(name2 + " done")
							files1= {'document': obj}

							response=session.post(url2 , data = {'description':name2}, files=files1)
							#print(name.split('/')[0]+'/'+name)
							decrypt_file(username,name)


			elif newScheme=='AES' or newScheme=='Salsa20' or newScheme=='ChaCha20':
				f = open("scheme_"+username+".txt", "w+")
				f.write(newScheme)
				f.close()
				key = Random.get_random_bytes(32)
				f = open("key_"+username+".txt","wb+")
				f.write(key)
				f.close()


				for i in range(0,len(fls)):
					fn=(str(fls[i]).split('<')[1]).split('>')[1]
					#print(fn)
					if fn==filename:
						hreff=fls[i+2].get("href")	
						#print(hreff)		
						urldel='http://'+host+str(hreff)
						q=session.get(urldel)
						#print(q)

						encrypt_file(username,name)

						url2= 'http://'+host+'/account/upload/'
						with open(name,'rb') as obj:
							name2=name.replace('^','/')
							print(name2)
							files1= {'document': obj}
							response=session.post(url2 , data = {'description':name2}, files=files1 )
							decrypt_file(username,name)
				#print('Successfully updated En-De scheme')
			else:
				print('Not a valid scheme')



							






		# 		print(oldScheme+' scheme already in use')
		# 	elif newScheme=='AES' or newScheme=='Blowfish' or newScheme=='ChaCha20':
		# 		f = open("scheme_"+username+".txt", "w+")
		# 		f.write(newScheme)
		# 		f.close()
		# 		key = Random.get_random_bytes(32)
		# 		f = open("key_"+username+".txt","wb+")
		# 		f.write(key)
		# 		f.close()
		# 		print('Successfully updated En-De scheme')
		# 	else:
		# 		print('Not a valid scheme')
		# else:
		# 	if newScheme=='AES' or newScheme=='Blowfish' or newScheme=='ChaCha20':
		# 		f = open("scheme_"+username+".txt", "w+")
		# 		f.write(newScheme)
		# 		f.close()
		# 		key = Random.get_random_bytes(32)
		# 		f = open("key_"+username+".txt","wb+")
		# 		f.write(key)
		# 		f.close()
		# 		print('Successfully changed En-De scheme')
		# 	else:
		# 		print('Not a valid scheme')


		#File is downloaded.
		#CHANGE THE ENCRYPTION SCHEME HERE
		#DELETE CORRESPONDING FILE ON WEB CLIENT AND UPLOAD IT


	#Lets deal with folders now


	# x=len(folders)
	# a=0
	# for i in range(0,x):
	# 	if folders[a] in files_download:
	# 		folders.remove(folders[a])
	# 	elif folders[a] in files:
	# 		folders.remove(folders[a])
	# 	else:
	# 		a=a+1
	# for i in range(0,len(folders)):
	# 	h=folders[i].get("href")
	# 	url2="http://'+host+'"+h
	# 	print(url2)
	# 	request_f=session.get(url2)
	# 	print(request_f)

	# 	soup = BeautifulSoup(request2.text,'html.parser')
	# 	files = soup.find(attrs={'class':'container'}).find_all('a',attrs={'class':'display_link'})
	# 	files_download = soup.find(attrs={'class':'container'}).find_all('a',attrs={'class':'download_link'})
	# 	folders = soup.find(attrs={'class':'container'}).find_all('a')


	# #Lets deal with files first:
	# 	files_web=[]
	# 	Href_web=[]
	# 	dict_href={}
	# 	for i in range(0,len(files)):		
	# 		filename=(str(files[i]).split('<')[1]).split('>')[1]
	# 		#print(filename)
	# 		files_web.append(filename)
	# 		Href=files[i].get("href")
	# 		Href_web.append(Href)
	# 		dict_href[filename]=str(Href)
	# 		p2=requests.get(urljoin("http://'+host+'", str(Href)))
	# 		with open(filename,"wb") as t:
	# 			t.write(p2.content)















		#Now look for files in the current folder:


		

		#with open("temp","wb") as t:
	# 				t0.write(p2.content)
	# 			f3=open('temp','rb')
	# 			s3=f3.read()
	# 			#print(s3)
	# 			hash_web=(hashlib.md5(s3).hexdigest())
	

	# if os.path.isdir(directory):
	# 	for (dirpath, dirnames, filenames) in os.walk(directory):
	# 		onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
	# 		#print(onlyfiles)
	# 		url1="http://'+host+'/account/profile2/"+dirpath
	# 		request2 = session.get(url1)
	# 		soup = BeautifulSoup(request2.text,'html.parser')
	# 		files = soup.find(attrs={'class':'container'}).find_all('a',attrs={'class':'display_link'})
	# 		# print(files)

	# 		#Now check for server to client
	# 		files_web=[]
	# 		Href_web=[]
	# 		dict_href={}
	# 		for i in range(0,len(files)):		
	# 			filename=(str(files[i]).split('<')[1]).split('>')[1]
	# 			#print(filename)
	# 			files_web.append(filename)
	# 			Href=files[i].get("href")
	# 			Href_web.append(Href)
	# 			dict_href[filename]=str(Href)
	# 			p2=requests.get(urljoin("http://'+host+'", str(Href)))
	# 			with open("temp","wb") as t:
	# 				t.write(p2.content)
	# 			f3=open('temp','rb')
	# 			s3=f3.read()
	# 			#print(s3)
	# 			hash_web=(hashlib.md5(s3).hexdigest())
					
	# 			temp=dirpath+"/"+filename
	# 			if filename not in onlyfiles:
	# 				with open(temp,"wb") as t:
	# 					t.write(p2.content)
	# 				print("Downloaded "+temp)
		
	# 			else: #implies the same file exists in both
	# 				f=open(temp,'rb')
	# 				s=f.read()
	# 				hash_client=(hashlib.md5(s).hexdigest())
	# 				if hash_client==hash_web:
	# 					print("File " + temp +" matched")
	# 				else:
	# 					#Do delete and upload

	# 					print("Delete")
	# 			#print(files_web)			
	# 		for i in onlyfiles:
	# 			temp=dirpath+"/"+i
	# 			if i not in files_web:
	# 				url1= 'http://'+host+'/account/upload/'
	# 				with open(temp,'rb') as obj:
	# 					files= {'document': obj}
	# 					response=session.post(url1 , data = {'description':temp}, files=files)
	# 				print(temp + " is uploaded")
	# 			else:
	# 				filepath1="http://'+host+'"+dict_href[i]
	# 				p2=requests.get(filepath1)
	# 				with open("temp","wb") as t:
	# 					t.write(p2.content)
	# 				f3=open('temp','rb')
	# 				s3=f3.read()
	# 				web_hash=(hashlib.md5(s3).hexdigest())
	# 				f=open(temp,'rb')
	# 				s=f.read()
	# 				client_hash=(hashlib.md5(s).hexdigest())
	# 				if(client_hash==web_hash):
	# 					print("File " + temp + " matched")
					
	# 				else:
	# 					print("Delete")
	# 					#do delete and replace
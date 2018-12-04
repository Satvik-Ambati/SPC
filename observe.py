import requests
import getpass
import re
import os
import sys
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from os import listdir
from os.path import isfile, join


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
#LOGIN DONE

directory = sys.argv[1]
directory = directory.split('/')[-1]

if len(ans)==1:
	print("Successfully logged in")
	with open("observe.txt","w") as f:
		f.write(directory)
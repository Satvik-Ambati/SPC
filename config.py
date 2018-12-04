import requests
import getpass
import re


f=open('url.txt','r')
host = f.read()[:]
f.close()

username = input('Username:')
pswd = getpass.getpass('Password:')
# print(pswd)
url= 'http://'+host+'/account/login/'
request = requests.post(url, data = {'username':username , 'password':pswd})
res = request.text

ans = re.findall("(Secure Personal Cloud)",res)
f=open("login_credentials.txt","w")
if len(ans)==1:
	f.write("1")
	print("Successfully logged in")
	f.write("\n" + username)
else:
	f.write("2")
	print("Invalid login credentials")
f.close()

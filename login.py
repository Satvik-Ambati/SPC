import requests
import getpass
import re

username = input('Username:')
pswd = getpass.getpass('Password:')


f=open('url.txt','r')
host = f.read()[:]
f.close()

f=open("login_details.txt","w")

# print(pswd)
url= 'http://'+host+'/account/login/'
print(url)
#print(url)
request = requests.post(url, data = {'username':username , 'password':pswd})
res = request.text
#print(res)

ans = re.findall("(Secure Personal Cloud)",res)
if len(ans)==1:
	print("Successfully logged in")
	f.write(username)
	f.write('\n'+pswd)
	
else:
	print("Invalid login credentials")
f.close()
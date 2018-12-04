import requests
import getpass
import re
import os

if (os.stat("login_details.txt").st_size == 0):
	print("You aren't logged in bro")

else:
	f=open("login_details.txt","w")
	f.close() 
	print("Successfully logged out")
#!/usr/bin/python3

url = input("Enter the ip address and the port of the server")
f = open('url.txt', 'w+')
f.write(url)
f.close()
print('URL successfully registered')
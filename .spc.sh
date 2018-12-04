#! /bin/bash

function spc(){
	if [ $1 == "login" ]; then
		python3 ~/SPC/login.py 
	elif [ $1 == "upload" ]; then
		python3 ~/SPC/upload.py
	elif [ $1 == "logout" ]; then
		python3 ~/SPC/logout.py
	elif [ $1 == "observe" ]; then
		python3 ~/SPC/observe.py $2
	elif [ $1 == "sync" ]; then
		python3 ~/SPC/sync.py
	elif [ $1 == "status" ]; then
		python3 ~/SPC/status.py
	elif [ "$1" == "version" ]; then
		echo '0.2.3'

	elif [ "$1" == "server" -a "$2" == "set-url" ]; then
		python3 ~/SPC/set-url.py

	elif [ "$1" == "server" ]; then
		cat url.txt | cut -d ':' -f 1
		echo 'port: 8000'

	elif [ "$1" == "help" ]; then
		man spc

	

	elif [ "$1" == 'en-de' -a "$2" == 'list' ]; then
	 	python3 ~/SPC/list.py 

	elif [ "$1" == 'en-de' -a "$2" == 'update' ]; then
		python3 ~/SPC/update.py


	elif [ $1 == "config" -a $2 == "edit" ]; then
		python3 ~/SPC/config.py 
		line=$(head -1 ~/SPC/login_credentials.txt)
		user=$(head -2 ~/SPC/login_credentials.txt | tail -1)
		if [ $line == "2" ]; then
			echo "Invalid Credentials"
		else
			python3 ~/SPC/manage.py changepassword $user
		fi
	fi	
}

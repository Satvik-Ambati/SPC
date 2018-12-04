#!/bin/bash
sudo apt-get install python3.7 python3-pip && pip3 install -r requirements.txt && sudo cp spc.1 /usr/share/man/man1 && echo 'source ~/SPC/.spc.sh' | cat >> ~/.bashrc;
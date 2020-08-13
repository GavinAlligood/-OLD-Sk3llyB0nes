import socket
import sys
import os
from colorama import Fore, Back, Style
import notify2
import nmap

print(" _____ _    _____ _ _      ______  _____ ")
print("/  ___| |  |____ | | |     | ___ \|  _  | ")
print("\ `--.| | __   / / | |_   _| |_/ /| |/' |_ __   ___  ___ ")
print(" `--. \ |/ /   \ \ | | | | | ___ \|  /| | '_ \ / _ \/ __| ")
print("/\__/ /   <.___/ / | | |_| | |_/ /\ |_/ / | | |  __/\__ \ ")
print("\____/|_|\_\____/|_|_|\__, \____/  \___/|_| |_|\___||___/ ")
print("                       __/ | ")
print("                      |___/ ")

####                                                                                                               ####
#### Only difference in 'iOS version' is that there is no notification module since i had trouble with that on iOS ####
####                                                                                                               ####

# Create socket
def gather_bones():
	try:
		global host
		global port
		host =''
		port = port
		s = socket.socket()
	except socket.error as msg:
		print(Style.BRIGHT + Fore.RED + "[☠] Socket creation error: " + str(msg) + Style.RESET_ALL)
	except NameError:
		print(Style.BRIGHT + Fore.RED + "[☠] Port not defined!" + Style.RESET_ALL)
		main()


# Bind socket to port and wait for connection
def connect_bones():
	try:
		global host
		global port
		global s
		s = socket.socket()
		print(Style.BRIGHT + Fore.BLUE + "[i] Binding socket to port: " + str(port) + Style.RESET_ALL)
		s.bind((host, port))
		s.listen(5) # number of bad connections
	except socket.error as msg:
		print(Style.BRIGHT + Fore.RED + "[☠] Socket binding error: " + str(msg) + "\n" + "Retrying..." + Style.RESET_ALL)
		socket_bind()

# Connect
def create_skeleton():
	# socket MUST be listening before it can accept
	conn, address = s.accept()
	print(Style.BRIGHT + Fore.BLUE + "[i] Connected to " + address[0] + ':' + str(port) + Style.RESET_ALL)
	command_skeleton(conn)
	# handle broken pipe exception !!!
	conn.close()

def command_skeleton(conn):
	while True:
		try:
			cmd = input()
			if cmd == 'quit':
				conn.close()
				s.close()
				# handle ctrl + c exception so sockets actually close
				#sys.exit()
				main()
			# system commands are stored as bytes thats why you must encode them
			if len(str.encode(cmd)) > 0:
				conn.send(str.encode(cmd))
				client_response = str(conn.recv(10000), "utf-8")
				print(client_response, end="") # end='': dont give a new line at the end of cmd
		except KeyboardInterrupt:
			print("") # Another empty line
			print("\n" + Style.BRIGHT + Fore.BLUE + "[i] Type 'quit' to close shell" + Style.RESET_ALL)
			continue

#nmap scan module
def scan(addr):
	try:
		scanner = nmap.PortScanner()
		scanner.scan(addr, '1-1000')
		print(Style.BRIGHT + Fore.BLUE + "[i] Host found: " + Fore.WHITE + scanner[addr].hostname() + Style.RESET_ALL)
		if scanner[addr].state() == "up":
			print(Style.BRIGHT + "[i] Status: " + Fore.GREEN + "Up" + Style.RESET_ALL)
		elif scanner[addr].state() == "down":
			print(Style.BRIGHT + "[i] Status: " + Fore.RED + "Down" + Style.RESET_ALL)
		elif scanner[addr].state() == "unkown":
			print(Style.BRIGHT + "[i] Status: " + Fore.YELLOW + "Unkown" + Style.RESET_ALL)
		else:
			print(Style.BRIGHT + Fore.RED + "[☠] An unkown error occured" + Style.RESET_ALL)

		print("\n" + Style.BRIGHT + Fore.BLUE + "[i] Open ports: " + Fore.WHITE)
		print("[i] Protocol: " + scanner[addr].all_protocols()[0])
		for p in scanner[addr]['tcp'].keys():
			print("[i] Open port: " + str(p))
		print(Style.RESET_ALL)
		

	except KeyError:
		print("\n" + Style.BRIGHT + Fore.RED + "[☠] Host not specified or invalid host!" + Style.RESET_ALL + "\n")


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
					try:
						print(Style.BRIGHT)
						if int(cmd[5:]) > 65353 or int(cmd[5:]) < 1:
							print(Style.BRIGHT + Fore.RED + "[☠] You cannot use a port below 1 or above 65353" + Style.RESET_ALL + "\n")
						else:
							port = int(cmd[5:])
							print(Style.BRIGHT + Fore.BLUE + "[i] Port set to: " + str(port) + Style.RESET_ALL + "\n")
					except ValueError:
						## neccessary because a number with comma not counted as base 10 decimal
						print(Style.BRIGHT + Fore.RED + "[☠] You cannot use a port below 1 or above 65353" + Style.RESET_ALL + "\n")
						continue
				elif cmd[:4].lower() == "scan":
					# name error exception needs to be handled: no host!
					scan(cmd[5:])
				elif cmd.lower() == "help":
					print("\nlisten - Start listening on specified port")
					print("port - Specify what port to listen on, for example: port 1337")
					print("exit - closes the application")
					print("scan - scan a host for open ports. Example: scan 127.0.0.1")
					print("clear/cls - clears screen (cls for windows, clear for linux)\n")
				elif cmd.lower() == "exit":
					sys.exit()

				else:
					print("\n" + Style.BRIGHT + Fore.RED + "☠ Get your bones together!! ☠" + Style.RESET_ALL + "\n")
		except KeyboardInterrupt:
			print("") # empty line for asthetic purposes
			print("\n" + Style.BRIGHT + Fore.BLUE + "[i] Type exit to close program" + Style.RESET_ALL + "\n")
			continue

main()

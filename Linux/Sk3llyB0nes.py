import socket
import sys
import os
from colorama import Fore, Back, Style
import notify2
import nmap
import requests
import subprocess

print(" _____ _    _____ _ _      ______  _____ ")
print("/  ___| |  |____ | | |     | ___ \|  _  | ")
print("\ `--.| | __   / / | |_   _| |_/ /| |/' |_ __   ___  ___ ")
print(" `--. \ |/ /   \ \ | | | | | ___ \|  /| | '_ \ / _ \/ __| ")
print("/\__/ /   <.___/ / | | |_| | |_/ /\ |_/ / | | |  __/\__ \ ")
print("\____/|_|\_\____/|_|_|\__, \____/  \___/|_| |_|\___||___/ ")
print("                       __/ | ")
print("                      |___/ ")

### Run in background Unix: python3 myfile &

### simply raising the ammount of bytes sent changes things... mess with this and monitor network resources being used 

conf = open("skelly-bones.conf", "r+")
conf_lines = conf.readlines()

SEPARATOR = "<SEPARATOR>"

## Notification settings:
notify2.init("Sk3lly B0nes")

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
		print(Style.BRIGHT + Fore.BLUE + "[i] Binding socket to port: " + Fore.WHITE + str(port) + Style.RESET_ALL)
		s.bind((host, port))
		s.listen(5) # number of bad connections
	except socket.error as msg:
		print(Style.BRIGHT + Fore.RED + "\n" "[☠] Socket binding error: " + str(msg) + Style.RESET_ALL + "\n")
		main()

# Connect
def create_skeleton():
	try:
		# socket MUST be listening before it can accept
		conn, address = s.accept()
		print(Style.BRIGHT + Fore.BLUE + "[i] Connected to " + Fore.WHITE + address[0] + ':' + str(port) + Style.RESET_ALL)
		n = notify2.Notification("Shell opened!", message = 'Connection succesfully established')
		n.set_urgency(notify2.URGENCY_CRITICAL) # low, normal, critical
		n.show()
		command_skeleton(conn)
		conn.close()
	except BrokenPipeError:
		print(Style.BRIGHT + Fore.RED + "[☠] Broken Pipe. Closing shell" + Style.RESET_ALL + "\n")

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
		scanner.scan(addr, prts, arguments="-sV") # basically just a service scan
		print(Style.BRIGHT + Fore.BLUE + "[i] Host found: " + Fore.WHITE + scanner[addr].hostname() + Style.RESET_ALL)
		if scanner[addr].state() == "up":
			print(Style.BRIGHT + "[i] Status: " + Fore.GREEN + "Up" + Style.RESET_ALL)
		elif scanner[addr].state() == "down":
			print(Style.BRIGHT + "[i] Status: " + Fore.RED + "Down" + Style.RESET_ALL)
		elif scanner[addr].state() == "unkown":
			print(Style.BRIGHT + "[i] Status: " + Fore.YELLOW + "Unkown" + Style.RESET_ALL)
		else:
			print(Style.BRIGHT + Fore.RED + "[☠] An unkown error occured" + Style.RESET_ALL)

		try:
			print("\n" + Style.BRIGHT + Fore.BLUE + "[i] Open ports: " + Fore.WHITE)
			print("[i] Protocol: " + scanner[addr].all_protocols()[0])
			for p in scanner[addr]['tcp'].keys():
				print("[i] Open port: " + str(p) + "\tService: " + scanner[addr]['tcp'][p]['name']) # tcp only for now. This line prints service info

			print(Style.RESET_ALL)
		except IndexError:
			print(Style.BRIGHT + Fore.YELLOW + "[i] No open ports discovered" + Style.RESET_ALL)
		

	except KeyError as msg:
		print("\n" + Style.BRIGHT + Fore.RED + "[☠] Error with keyword: " + str(msg) + " Either invalid host or port range" + "\n")
		print("Correct usage example: scan 127.0.0.1\n")
		print("Port range: 55-1040" +  Style.RESET_ALL)

def write(word):
	f1 = open("log1.txt","a")
	f1.write(word +"\n")

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
				elif cmd[:4].lower() == "port":
					try:
						print(Style.BRIGHT)
						if int(cmd[5:]) > 65353 or int(cmd[5:]) < 1:
							print(Style.BRIGHT + Fore.RED + "[☠] You cannot use a port below 1 or above 65353" + Style.RESET_ALL + "\n")
						else:
							port = int(cmd[5:])
							print(Style.BRIGHT + Fore.BLUE + "[i] Port set to: " + Fore.WHITE + str(port) + Style.RESET_ALL + "\n")
					except ValueError:
						## neccessary because a number with comma not counted as base 10 decimal
						print(Style.BRIGHT + Fore.RED + "[☠] You cannot use a port below 1 or above 65353" + Style.RESET_ALL + "\n")
						continue
				elif cmd[:4].lower() == "scan":
					global prts
					prts = input(Style.BRIGHT + Fore.BLUE + "[i] Port range (blank for default 1000): " +  Style.RESET_ALL)
					if prts == "":
						prts = '1-1000'
						scan(cmd[5:])
					else:
						scan(cmd[5:])
				elif cmd.lower() == "devices":
					nm = nmap.PortScanner()
					host = input(Style.BRIGHT + Fore.BLUE + "[i] Enter your subnet: " + Style.RESET_ALL)
					nm.scan(hosts=host + '/24', arguments='n -sP -PE -PA21,23,80,3389')
					print(Style.BRIGHT + Fore.YELLOW + "Note: some hosts may block ping requests. Those that do will not show up here")
					for ip in nm.all_hosts():
						if nm[ip].state() == "up":
							print("\n" + Style.BRIGHT + Fore.BLUE + "[i] Host found: " + Fore.WHITE + nm[ip].hostname() + " | " + Fore.WHITE + ip + " | Status: " + Fore.GREEN + "Up")
						elif nm[ip].state() == "down":
							print("\n" + Style.BRIGHT + Fore.BLUE + "[i] Host found: " + Fore.WHITE + nm[ip].hostname() + " | " + Fore.WHITE + ip + " | Status: " + Fore.RED + "Down")
						else:
							print("\n" + Style.BRIGHT + Fore.BLUE + "[i] Host found: " + Fore.WHITE + nm[ip].hostname() + " | " + Fore.WHITE + ip + " | Status: " +  Fore.YELLOW + "Unkown")
					# not entirely sure if ill keep this up,down, and unkown stuff since it only prints the ones that are up
					print(Style.RESET_ALL) # also prints a new line as well as resetting the style
				elif cmd.lower() == "show port":
					try:
						print("\n" + Style.BRIGHT + Fore.BLUE + "[i] Listening port: " + Fore.WHITE + str(port))
						print(Style.RESET_ALL)
					except NameError:
						print("\n" + Style.BRIGHT + Fore.RED + "[☠] Listening port is not defined")
						print(Style.RESET_ALL)	
				elif cmd.lower() == "help":
					print(Style.BRIGHT + Fore.YELLOW)
					print("listen - Start listening on specified port")
					print("port - Specify what port to listen on, for example: port 1337")
					print("		- show port - shows the port used to listen")
					print("exit - closes the application")
					print("scan - scan a host for open ports. Example: scan 127.0.0.1")
					print("devices - lists active devices connected to your network.")
					print("ncat [port] - starts a netcat listener. Best for CTFS or pentests. example: ncat 45")
					print("dir [url] - starts a directory bruteforce on that url. example: dir http://eee.com/  wordlist: /home/user/Documents/wordlist.txt")
					print("clear/cls - clears screen (cls for windows, clear for linux)")
					print("show")
					print(Style.RESET_ALL)
				elif cmd[:3].lower() == "dir":
					try:
						url = cmd[4:]
						## dont forget this starts at 0 so '1' is line # 2
						list_limit = conf_lines[1]
						wordlist = input(Style.BRIGHT + Fore.BLUE + "[i] Wordlist path: " + Fore.WHITE)
						print(Fore.BLUE + "[i] Note that some urls beggining with # may be false positive, and the current list limit is: " + Fore.WHITE + str(list_limit) + Fore.BLUE + ". This may be changed in the config file" + Style.RESET_ALL)
						wl = open(wordlist)
						print(wl)
						for i in range(int(list_limit)):
							word = wl.readline(10).strip()
							furl = url+word
							response = requests.get(furl)
							if (response.status_code == 200):
								if furl != url:
									print(Style.BRIGHT + Fore.BLUE + "[i] Found: " + Fore.GREEN + furl + Style.RESET_ALL)
								write(furl)
							else:
								#print(Style.BRIGHT + Fore.BLUE + "[i] Not Found: " + Fore.RED + furl + Style.RESET_ALL)
								pass
					except FileNotFoundError:
						print(Style.BRIGHT + Fore.RED + "[☠] File not found" + Style.RESET_ALL)
					except:
						print(Style.BRIGHT + Fore.RED + "[☠] Invalid url or does not exist. Format should be http://url.com/" + Style.RESET_ALL + "\n")
				elif cmd[:4].lower() == "ncat":
					try:
						## ncat automatically handles too big or wrong ports. less work for me!
						print(Style.BRIGHT + Fore.BLUE + "[i] Setting port to: " + Fore.WHITE + cmd[5:])
						print(Fore.BLUE + "[i] Starting netcat listener")
						print(Style.RESET_ALL)
						print("[i] https://netsec.ws/?p=337 (How to get a tty shell)")
						os.system("nc -lvnp " + cmd[5:])
						
					except ValueError:
						print(Style.BRIGHT + Fore.RED + "[☠] Invalid port option" + Style.RESET_ALL + "\n")
				elif cmd.lower() == "ls":
					print(Style.BRIGHT + Fore.BLUE + "\n[i] Current directory: " + Fore.WHITE + os.getcwd() + "/" + Style.RESET_ALL + "\n")
					for file in os.listdir():
						print(file)
					print("\n")
				elif cmd.lower() == "exit":
					sys.exit()

				else:
					print("\n" + Style.BRIGHT + Fore.RED + "☠ Get your bones together!! ☠" + Style.RESET_ALL + "\n")
		except KeyboardInterrupt:
			print("") # empty line for asthetic purposes
			print("\n" + Style.BRIGHT + Fore.BLUE + "[i] Type exit to close program" + Style.RESET_ALL + "\n")
			continue

main()
conf.close()

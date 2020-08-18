import socket
import sys
import os
from colorama import Fore, Back, Style
from plyer import notification
import nmap

#### WINDOWS VERSION ####

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
        print(Style.BRIGHT + Fore.RED + "\n" "[☠] Socket binding error: " + str(msg) + Style.RESET_ALL + "\n")
        main()

# Connect
def create_skeleton():
    try:
        # socket MUST be listening before it can accept
        conn, address = s.accept()
        print(Style.BRIGHT + Fore.BLUE + "[i] Connected to " + address[0] + ':' + str(port) + Style.RESET_ALL)
        notification.notify(title='Shell opened!', message='Connection succesfully established', app_icon=None, timeout=2)
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
                    global prts
                    prts = input(Style.BRIGHT + Fore.BLUE + "[i] Port range (blank for default 1000): " +  Style.RESET_ALL)
                    if prts == "":
                        prts = '1-1000'
                        scan(cmd[5:])
                    else:
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

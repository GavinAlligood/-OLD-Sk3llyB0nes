# Sk3llyB0nes
[WIP] hacking framework
Im creating Sk3llyB0nes to help automate things while i do penetration testing/ctfs.

Im focusing On Linux right now, and i will add all the features to windows sometime later and all the features i CAN add to iOS i will

If the shell gets stuck just hit ctrl + c and then commands should keep executing normally

NOTE: iOS (and windows) are seperate because of notification modules. The reason is because i use notify2 which uses dbus which you makes problems on windows and iOS for that matter. (non jailbroken) iOS also has problems with nmap. There is a usefull app called fing on iOS which lets you view devices on your network and scan them for ports so until i have another solution that is what you can use for iOS scanning features on Sk3llyB0nes. Im running this script on iSH on my iphone (beta app. Ive installed pip and everything succesfully): https://ish.app/

i will soon organize the files better as well

thanks to: thenewboston for initial reverse shell code. You taught me alot

How to use reverse shell functionality:

Set the port you would like to listen to with the port command

port <number>

for example, port 4444

Then type Listen to start listening for connections.

On the target machine, run rev.py and enter the IP and port you chose to listen on. These can be added into the code to avoid having to type those.

You should then recieve a connection on Sk3llyB0nes and you can then use normal reverse shell features, along with these commands:

download - prompts you to download a file remotely from victims machine. These are stored in the /downloads folder
upload - upload a file to victims machine (not fully functional yet, crashes Sk3lly socket connection)
screenshot - takes a screenshot of the victims machine. You will have to download it. They start of labeled "Shot1" then "Shot2", etc.

use the 'help' command inside the framework to view other things the framework can do

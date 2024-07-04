# Sk3llyB0nes
"Sk3llyB0nes" is a hacking tool I made when I was 14 or so
I might mess around with it for fun but I don't think I will put much effort into actually improving or fixing it, it's really just an old project

If the shell gets stuck try hitting ctrl + c

## How to use reverse shell functionality:

### On the hacker's computer, run Sk3llyB0nes.py and specify the port you would like to listen to with the port command

port <number>

for example, port 4444

### Then use the Listen command to start listening for connections.

### On the target machine, run rev.py and enter the IP and port you chose to listen on. 

*Note: This isn't practical or ideal in any real "hacking" scenario, but this tool is mostly just for show anyway*

*This could be improved by writing the target's IP and chosen port into Rev.py*

### You should then receive a connection on the device running Sk3llyB0nes and you can then use normal reverse shell features, along with these commands:

Download - Prompts you to download a file remotely from the target's device. These are stored in the /downloads folder.

(not functional) Upload - Upload a file to the target's machine.

Screenshot - Takes a screenshot of the target's machine. They start labeled "Shot1" then "Shot2", etc.

*Note: Re-reading this, screenshots seem to be saved automatically on the target's device which means the hacker would have to also download them manually from the victim's device using the download command.*
*I don't know why I wrote it to work like that, but I don't know If I will ever get around to fixing it either*

Use the 'help' command inside the framework to view other things the framework can do

## Screenshots:
![Image failed to load](/git_res/screenshot_skelly1.jpg?raw=true "Sk3lly simple usage")
![Image failed to load](/git_res/screenshot_skelly2.jpg?raw=true "Sk3lly simple usage")

# Sk3llyB0nes
[WIP] hacking framework
Im creating Sk3llyB0nes to help automate things while i do penetration testing/ctfs. I plan to add things like directory bruteforce, service/password bruteforce, etc

NOTE: iOS (and windows) are seperate because of notification modules. So the default python files in the main branch of the repository is for linux. The reason is because i use notify2 which uses dbus which you makes problems on windows and iOS for that matter. (non jailbroken) iOS also has problems with nmap. There is a usefull app called fing on iOS which lets you view devices on your network and scan them for ports so until i have another solution that is what you can use for iOS scanning features on Sk3llyB0nes. Im running this script on iSH on my iphone (beta app. Ive installed pip and everything succesfully): https://ish.app/

i will soon organize the files better as well

thanks to: thenewboston for initial reverse shell code. You taught me alot

note: not a tty shell sadly. It will have file transfer soon though. Also, changing directories in the reverse shell DOES work, even if it says 'cant cd to...' youll notice it does change to that directory

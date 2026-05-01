1. Install Python (if you don’t already have it)
Head over to: https://www.python.org/downloads/
Grab Python 3.9+ (honestly, anything fairly recent should be fine)
Important: during install, make sure you check “Add Python to PATH”

2. Double-check Python works
Open Command Prompt

Run:

python --version

You should see something like:

Python 3.x.x
Running the Script
Step 1: Open Command Prompt as Admin
Press Win + R
Type cmd
Hit Ctrl + Shift + Enter (not just Enter — this matters)
Accept the prompt

Yeah, admin rights are required here or things will fail in weird ways.

Step 2: Go to the Script Folder
cd path\to\mac-spoofer

(Replace "path\to\mac-spoofer" with the actual folder where you downloaded it)


Step 3: See Available Network Adapters
python mac_spoofer.py --list

This will show you the exact adapter names — you’ll need them later.

Step 4: Change MAC Address
python mac_spoofer.py --adapter "Ethernet" --mac "AA:BB:CC:DD:EE:FF"

Just swap:

"Ethernet" → whatever your adapter is actually called
"AA:BB:CC:DD:EE:FF" → the MAC you want
Common Things You’ll Probably Do
List adapters (again, because you’ll forget the name)
python mac_spoofer.py --list
Random MAC for Wi-Fi
python mac_spoofer.py --adapter "Wi-Fi" --random
Reset Ethernet back to original
python mac_spoofer.py --adapter "Ethernet" --reset
Use a custom MAC
python mac_spoofer.py --adapter "Ethernet" --mac "00-11-22-33-44-55"

(Both colon and dash formats usually work, but depends on how the script handles it.)

After Changing the MAC

Sometimes it applies instantly… sometimes it doesn’t. If nothing changed, try one of these:

Option 1 (GUI way)
Settings -> Network & Internet
Find your adapter
Go to Change adapter options
Disable -> Enable
Option 2 (CLI way)
ipconfig /release
ipconfig /renew
Option 3 (the “just reboot it” method)
shutdown /r /t 0

Honestly, this fixes most weird cases.

Check If It Worked
Open Command Prompt (normal is fine)

Run:

ipconfig /all
Look for:
Physical Address

If it matches what you set than you’re good :>

Troubleshooting (aka the usual headaches)
Problem	What to try
Needs admin privileges	You probably didn’t run CMD as admin
Adapter not found	Run --list again and copy-paste the name
MAC didn’t change	Restart adapter or reboot
Access denied	Try disabling antivirus temporarily (yeah… not ideal, but happens)
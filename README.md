MAC Address Spoofer (Windows)

A simple little tool to change your network adapter’s MAC address on Windows. No extra dependencies, no fluff — just does what it needs to.

Requirements Windows (10, 11) Python 3.6+ (3.9+ is probably better) Important: check “Add Python to PATH” during install Administrator privileges (this is required, not optional) PowerShell (already included in Windows) No external packages — just standard library What it can do List network adapters (and show current MAC addresses) Change/spoof a MAC address Reset back to the original hardware MAC Generate a random MAC(wayeasizer then typing one lowk) Simple CLI — nothing fancy Installation

Install Python (if needed) Download from: https://www.python.org/downloads/ Install Python 3.6+ Make sure to check “Add Python to PATH”
Verify:

python --version

Download this repo Click “Code” -> “Download ZIP” or
Clone it:

git clone

Open the folder Open the folder in File Explorer Shift + Right-click → “Open PowerShell window here” (or Command Prompt)
Easiest way is just to double-click: run.bat

This will:

Open Command Prompt as admin Show available adapters Give you example commands Manual way (Command Prompt) Run Command Prompt as Administrator

Navigate to folder:

cd path\to\mac-spoofer

Commands List adapters

python mac_spoofer.py --list

You’ll use this a lot to get adapter names.

Change MAC address

python mac_spoofer.py --adapter "Ethernet" --mac "AA:BB:CC:DD:EE:FF"

Supported formats:

AA:BB:CC:DD:EE:FF AA-BB-CC-DD-EE-FF AABBCCDDEEFF

(Colon format is easiest IMO)

Random MAC

python mac_spoofer.py --adapter "Ethernet" --random

Probably the most convenient option.

Reset MAC

python mac_spoofer.py --adapter "Ethernet" --reset

Good if something breaks or you want to undo changes.

CLI Options

--list List adapters --adapter Target adapter name --mac Set custom MAC --random Generate random MAC --reset Restore original MAC

Example Output
AVAILABLE NETWORK ADAPTERS Ethernet Current MAC Address: 00-1A-2B-3C-4D-5E Wi-Fi Current MAC Address: A0-1B-2C-3D-4E-5F

======================================================================

After Changing the MAC

Sometimes it works instantly… sometimes not.

If nothing changes:

Disable/Enable the adapter

Run:

ipconfig /release ipconfig /renew

Or just reboot

Honestly, rebooting fixes it most of the time.

Important Notes

Admin required If you’re not running as admin, it will fail (usually with vague errors)

Registry changes This modifies Windows registry values tied to adapters Not dangerous if you know what you're doing, but still worth noting

Legal stuff Don’t use this on networks without permission MAC spoofing can violate policies/laws depending on context

How it works (quick version) Uses PowerShell (Get-NetAdapter) to get adapter info Writes to the NetworkAddress registry key Changes apply after restarting adapter or reboot

Nothing too complex behind the scenes.

Troubleshooting

Requires admin privileges You didn’t run as admin Restart terminal as Administrator

Could not find adapter Run --list Copy the exact name

MAC didn’t change Restart adapter Or run:

ipconfig /release ipconfig /renew

Or reboot

Access denied Make sure you’re admin Antivirus might be interfering

Supported Windows Versions Windows 10 Windows 11 Windows Server 2016+

(Older versions might work, just not tested)

Disclaimer

This tool is for:

Network testing Debugging Learning

If you misuse it, that’s on you. Make sure you have permission before using it.

Notes Code could probably be cleaned up a bit If something breaks… it might just be Windows being Windows Support (sort of)

If things aren’t working:

Check admin privileges Make sure Python is installed correctly Confirm PowerShell works Double-check adapter names

After that… yeah, might require some debugging.

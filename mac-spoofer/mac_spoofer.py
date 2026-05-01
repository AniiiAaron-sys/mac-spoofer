
#MAC Address Spoofer for Windows


import subprocess
import re
import sys
import argparse
from typing import List, Tuple, Optional
import ctypes
import os


class MACSpoofer:
    
    def __init__(self):
        self.adapters = {}
        self.check_admin()
    
    @staticmethod
    def check_admin() -> bool:
        """Check if the script is running with administrative privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def get_adapters(self) -> dict:
        """
        Get all network adapters and their current MAC addresses.
        Returns a dictionary with adapter names as keys and MAC addresses as values.
        """
        
        try:
            result = subprocess.run(
                ['ipconfig', '/all'],
                capture_output=True,
                text=True,
                check=True
            )
            
            adapters = {}
            current_adapter = None
            
            for line in result.stdout.split('\n'):
                # Match adapter names
                if line and not line[0].isspace():
                    current_adapter = line.strip().rstrip(':')
                
                # Match MAC addresses (Physical Address)
                if 'Physical Address' in line and current_adapter:
                    mac_match = re.search(r'([0-9A-Fa-f]{2}-){5}([0-9A-Fa-f]{2})', line)
                    if mac_match:
                        mac_address = mac_match.group(0)
                        adapters[current_adapter] = mac_address
            
            self.adapters = adapters
            return adapters
        
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving adapters: {e}")
            return {}
    
    def list_adapters(self) -> None:
        """Display all network adapters and their current MAC addresses."""
        adapters = self.get_adapters()
        
        if not adapters:
            print("No network adapters found or unable to retrieve adapter information.")
            return
        
        print("\n" + "="*70)
        print("AVAILABLE NETWORK ADAPTERS")
        print("="*70)
        
        for idx, (adapter, mac) in enumerate(adapters.items(), 1):
            print(f"\n{idx}. {adapter}")
            print(f"   Current MAC Address: {mac}")
        
        print("\n" + "="*70 + "\n")
    
    @staticmethod
    def validate_mac(mac: str) -> bool:
        """
        Validate MAC address format.
        Accepts formats: XX:XX:XX:XX:XX:XX, XX-XX-XX-XX-XX-XX, XXXXXXXXXXXX
        """
        mac = mac.replace(':', '').replace('-', '')
        
        if len(mac) != 12:
            return False
        
        try:
            int(mac, 16)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def format_mac(mac: str) -> str:
        """Format MAC address to XX-XX-XX-XX-XX-XX format."""
        mac = mac.replace(':', '').replace('-', '').upper()
        
        if len(mac) != 12:
            raise ValueError("Invalid MAC address length")
        
        return '-'.join([mac[i:i+2] for i in range(0, 12, 2)])
    
    def change_mac(self, adapter_name: str, new_mac: str) -> bool:
        """
        Change the MAC address of a specific adapter via direct registry write.
        Requires administrative privileges.
        """
        if not self.validate_mac(new_mac):
            print(f"Error: Invalid MAC address format: {new_mac}")
            return False

        formatted_mac = self.format_mac(new_mac)
        mac_raw = formatted_mac.replace("-", "")

        # PowerShell script:
        # 1. Find the adapter by name
        # 2. Match its GUID to the correct registry subkey
        # 3. Write NetworkAddress directly
        # 4. Restart the adapter so the change takes effect
        ps_script = f"""
$adapterName = "*{adapter_name}*"
$adapter = Get-NetAdapter | Where-Object {{ $_.Name -like $adapterName }} | Select-Object -First 1
if (-not $adapter) {{
    Write-Error "Adapter not found: {adapter_name}"
    exit 1
}}
$guid = $adapter.InterfaceGuid
$regBase = "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}"
$found = $false
Get-ChildItem $regBase -ErrorAction SilentlyContinue | ForEach-Object {{
    $key = $_
    $id = (Get-ItemProperty $key.PSPath -Name "NetCfgInstanceId" -ErrorAction SilentlyContinue).NetCfgInstanceId
    if ($id -eq $guid) {{
        Set-ItemProperty -Path $key.PSPath -Name "NetworkAddress" -Value "{mac_raw}" -Type String
        $found = $true
    }}
}}
if (-not $found) {{
    Write-Error "Registry key not found for adapter GUID $guid"
    exit 1
}}
Disable-NetAdapter -Name $adapter.Name -Confirm:$false
Start-Sleep -Milliseconds 1500
Enable-NetAdapter -Name $adapter.Name
Write-Output "OK"
"""

        try:
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_script],
                capture_output=True,
                text=True
            )

            if result.returncode == 0 and "OK" in result.stdout:
                print(f"\nSuccess! MAC address changed for adapter '{adapter_name}'")
                print(f"New MAC Address: {formatted_mac}")
                print("Adapter was restarted automatically.")
                return True
            else:
                print(f"Error: Failed to change MAC address")
                print(f"Details: {result.stderr.strip() or result.stdout.strip()}")
                return False

        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def reset_mac(self, adapter_name: str) -> bool:
        """
        Reset the MAC address of an adapter to its original hardware address
        by removing the NetworkAddress registry value entirely.
        """
        ps_script = f"""
$adapterName = "*{adapter_name}*"
$adapter = Get-NetAdapter | Where-Object {{ $_.Name -like $adapterName }} | Select-Object -First 1
if (-not $adapter) {{
    Write-Error "Adapter not found: {adapter_name}"
    exit 1
}}
$guid = $adapter.InterfaceGuid
$regBase = "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}"
$found = $false
Get-ChildItem $regBase -ErrorAction SilentlyContinue | ForEach-Object {{
    $key = $_
    $id = (Get-ItemProperty $key.PSPath -Name "NetCfgInstanceId" -ErrorAction SilentlyContinue).NetCfgInstanceId
    if ($id -eq $guid) {{
        Remove-ItemProperty -Path $key.PSPath -Name "NetworkAddress" -ErrorAction SilentlyContinue
        $found = $true
    }}
}}
if (-not $found) {{
    Write-Error "Registry key not found for adapter GUID $guid"
    exit 1
}}
Disable-NetAdapter -Name $adapter.Name -Confirm:$false
Start-Sleep -Milliseconds 1500
Enable-NetAdapter -Name $adapter.Name
Write-Output "OK"
"""

        try:
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_script],
                capture_output=True,
                text=True
            )

            if result.returncode == 0 and "OK" in result.stdout:
                print(f"\nSuccess! MAC address reset for adapter '{adapter_name}'")
                print("The adapter will now use its original hardware MAC address.")
                print("Adapter was restarted automatically.")
                return True
            else:
                print(f"Error: Failed to reset MAC address")
                print(f"Details: {result.stderr.strip() or result.stdout.strip()}")
                return False

        except Exception as e:
            print(f"Error: {e}")
            return False


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description='MAC Address Spoofer for Windows\n'
                    'Change the MAC address of network adapters on Windows systems.\n'
                    'Requires administrative privileges.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
%(prog)s --list
    List all network adapters and their current MAC addresses

%(prog)s --adapter "Ethernet" --mac "AA:BB:CC:DD:EE:FF"
    Change MAC address of Ethernet adapter

%(prog)s --adapter "Ethernet" --reset
    Reset MAC address to original hardware address
        '''
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all network adapters and their current MAC addresses'
    )
    
    parser.add_argument(
        '--adapter',
        type=str,
        help='Name or partial name of the network adapter to modify'
    )
    
    parser.add_argument(
        '--mac',
        type=str,
        help='New MAC address (formats: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX)'
    )
    
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset MAC address to original hardware address'
    )
    
    parser.add_argument(
        '--random',
        action='store_true',
        help='Generate a random MAC address'
    )
    
    args = parser.parse_args()
    
    # Check for admin privileges
    if not MACSpoofer.check_admin():
        print("Error: This script requires administrative privileges.")
        print("Please run the script as administrator.")
        sys.exit(1)
    
    spoofer = MACSpoofer()
    
    # Handle --list argument
    if args.list:
        spoofer.list_adapters()
        return
    
    if args.random:
        import random
        mac_parts = [random.randint(0, 255) for _ in range(6)]
        mac_parts[0] = mac_parts[0] & 0xFE
        args.mac = ':'.join([f'{part:02X}' for part in mac_parts])
        print(f"Generated random MAC address: {args.mac}")
    
    # Validate arguments
    if not args.adapter:
        parser.print_help()
        sys.exit(1)
    
    # Handle MAC change
    if args.mac:
        spoofer.change_mac(args.adapter, args.mac)
    # Handle MAC reset
    elif args.reset:
        spoofer.reset_mac(args.adapter)
    else:
        print("Error: Please specify --mac, --reset, or --random")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

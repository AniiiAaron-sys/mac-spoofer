@echo off
REM MAC Spoofer - Quick Start Script
REM This script opens Command Prompt as Administrator and lists network adapters

echo Checking for Administrator privileges...

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires Administrator privileges.
    echo Attempting to restart as Administrator...
    powershell -Command "Start-Process cmd -ArgumentList '/k cd /d %cd% & python mac_spoofer.py --list' -Verb RunAs"
    exit /b
)

echo.
echo ========================================
echo MAC Spoofer - Available Adapters
echo ========================================
echo.
python mac_spoofer.py --list

echo.
echo ========================================
echo Quick Command Examples:
echo ========================================
echo.
echo 1. List all adapters:
echo    python mac_spoofer.py --list
echo.
echo 2. Change MAC address:
echo    python mac_spoofer.py --adapter "Ethernet" --mac "AA:BB:CC:DD:EE:FF"
echo.
echo 3. Generate random MAC:
echo    python mac_spoofer.py --adapter "Ethernet" --random
echo.
echo 4. Reset to original MAC:
echo    python mac_spoofer.py --adapter "Ethernet" --reset
echo.
pause

@echo off
REM MAC Spoofer - Setup Script
REM Verifies Python installation and displays setup information

cls
echo ========================================
echo MAC Spoofer - Setup Verification
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.6+ from: https://www.python.org/downloads/
    echo Important: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed:
python --version
echo.

echo [OK] Script location: %cd%
echo.

echo Checking for required files...
if exist "mac_spoofer.py" (
    echo [OK] mac_spoofer.py found
) else (
    echo [ERROR] mac_spoofer.py not found!
    pause
    exit /b 1
)

if exist "README.md" (
    echo [OK] README.md found
) else (
    echo [WARNING] README.md not found
)

if exist "run.bat" (
    echo [OK] run.bat found
) else (
    echo [WARNING] run.bat not found
)

echo.
echo ========================================
echo Setup verification complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: run.bat (to start using the tool)
echo 2. Or open Command Prompt as Administrator in this folder
echo 3. Then run: python mac_spoofer.py --list
echo.
pause

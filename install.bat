@echo off
echo Starting Hydra Print Automation Installation...

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install dependencies from local deps directory
echo Installing dependencies from local packages...
if not exist deps (
    echo Error: Local packages directory 'deps' not found.
    echo Please run 'python download_packages.py' first in environment with internet access to download the required packages.
    pause
    exit /b 1
)

pip install --no-index --find-links=file:./deps -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

REM Create necessary directories
if not exist logs mkdir logs

echo Installation completed successfully.
echo.
echo To run the application:
echo   python main.py
echo.
echo To configure automatic startup on login:
echo 1. Run manage_startup.bat
echo 2. Choose option 1 to add to Windows Startup
echo.
echo To run the application in the background (no console window):
echo   start_app.bat
echo.
pause
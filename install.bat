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

REM Install dependencies
echo Installing dependencies...
pip install --no-cache-dir -r requirements.txt
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
echo To install as a Windows service (requires administrator privileges):
echo 1. Run service_install.bat as administrator
echo.
pause
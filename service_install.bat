@echo off
setlocal enabledelayedexpansion
echo Installing Hydra Print Automation as Windows Service...

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrator privileges.
    echo Please run as administrator.
    pause
    exit /b 1
)

REM Check if NSSM is available
where nssm >nul 2>&1
if %errorLevel% neq 0 (
    echo NSSM is not installed. Please install NSSM first.
    echo Download from: https://nssm.cc/download
    echo After downloading, add NSSM to your system PATH or place nssm.exe in this directory.
    pause
    exit /b 1
)

REM Get Python path
for /f "tokens=*" %%a in ('python -c "import sys; print(sys.executable)"') do set PYTHON_PATH=%%a
if not defined PYTHON_PATH (
    echo Python executable not found. Make sure Python is installed and in your system PATH.
    pause
    exit /b 1
)

echo Using Python at: %PYTHON_PATH%

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "SERVICE_NAME=HydraPrintAutomation"
set "LOG_DIR=%CURRENT_DIR%logs"

echo Stopping and removing existing service if it exists...
net stop %SERVICE_NAME% >nul 2>&1
nssm remove %SERVICE_NAME% confirm >nul 2>&1
sc delete %SERVICE_NAME% >nul 2>&1

echo Installing new service...
nssm install %SERVICE_NAME% "%PYTHON_PATH%" "%CURRENT_DIR%main.py"
if %errorlevel% neq 0 (
    echo Failed to install service.
    pause
    exit /b 1
)

REM Configure service properties
nssm set %SERVICE_NAME% DisplayName "Hydra Print Automation Service"
nssm set %SERVICE_NAME% Description "Automates print operations for HYDRA system"
nssm set %SERVICE_NAME% Start SERVICE_AUTO_START
nssm set %SERVICE_NAME% AppDirectory "%CURRENT_DIR%"
nssm set %SERVICE_NAME% AppStdout "%LOG_DIR%\service.log"
nssm set %SERVICE_NAME% AppStderr "%LOG_DIR%\service_error.log"
nssm set %SERVICE_NAME% AppRestartDelay 5000

REM Create logs directory if it doesn't exist
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo Starting service...
net start %SERVICE_NAME%
if %errorlevel% neq 0 (
    echo Failed to start service. Check the logs for more information.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Service installed and started successfully!
echo Service Name: %SERVICE_NAME%
echo Python Path: %PYTHON_PATH%
echo Application Directory: %CURRENT_DIR%
echo Logs Directory: %LOG_DIR%
echo.
echo To manage the service:
echo - Start: net start %SERVICE_NAME%
echo - Stop: net stop %SERVICE_NAME%
echo - Restart: net stop %SERVICE_NAME% && net start %SERVICE_NAME%
echo - Uninstall: nssm remove %SERVICE_NAME% confirm
echo.
echo Press any key to exit...
pause >nul
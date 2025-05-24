@echo off
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
    pause
    exit /b 1
)

REM Stop and remove existing service if it exists
net stop HydraPrintAutomation >nul 2>&1
sc delete HydraPrintAutomation >nul 2>&1

REM Get the current directory
set "CURRENT_DIR=%~dp0"

REM Install the service
nssm install HydraPrintAutomation "%CURRENT_DIR%venv\Scripts\python.exe" "%CURRENT_DIR%main.py"
nssm set HydraPrintAutomation DisplayName "Hydra Print Automation Service"
nssm set HydraPrintAutomation Description "Automates AIP print operations for Hydra system"
nssm set HydraPrintAutomation Start SERVICE_AUTO_START
nssm set HydraPrintAutomation AppDirectory "%CURRENT_DIR%"
nssm set HydraPrintAutomation AppStdout "%CURRENT_DIR%service.log"
nssm set HydraPrintAutomation AppStderr "%CURRENT_DIR%service_error.log"

REM Start the service
net start HydraPrintAutomation

echo Service installation completed.
echo Service logs will be written to service.log and service_error.log
pause 
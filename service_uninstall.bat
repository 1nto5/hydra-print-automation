@echo off
setlocal enabledelayedexpansion

echo Uninstalling Hydra Print Automation Service...
set "SERVICE_NAME=HydraPrintAutomation"

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrator privileges.
    echo Please run as administrator.
    pause
    exit /b 1
)

echo Stopping service if running...
net stop %SERVICE_NAME% >nul 2>&1

REM Remove service using NSSM if available
where nssm >nul 2>&1
if %errorLevel% == 0 (
    nssm remove %SERVICE_NAME% confirm >nul 2>&1
) else (
    sc delete %SERVICE_NAME% >nul 2>&1
)

echo Service has been uninstalled.
echo.
echo Note: Application files and logs have not been removed.
echo To completely remove the application, delete the installation directory.
echo.
pause

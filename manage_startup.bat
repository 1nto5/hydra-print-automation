@echo off
setlocal enabledelayedexpansion

:: Hydra Print Automation
:: This script manages the Windows startup configuration for the Hydra Print Automation service

REM Set paths and configuration
set "SCRIPT_DIR=%~dp0"
set "BATCH_FILE=start_app.bat"
set "SHORTCUT_NAME=Hydra Print Automation.lnk"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

:menu
cls
echo =======================================
echo  Hydra Print Automation - Startup Manager
echo =======================================
echo 1. Add to Windows Startup
echo 2. Remove from Windows Startup
echo 3. Exit
echo.
set "choice="
set /p "choice=Choose an option: "

if "%choice%"=="" goto menu
if "%choice%"=="1" goto add_startup
if "%choice%"=="2" goto remove_startup
if "%choice%"=="3" goto end
goto menu

:add_startup
if not exist "%SCRIPT_DIR%%BATCH_FILE%" (
    echo.
    echo [ERROR] Could not find %BATCH_FILE% in the current directory
    echo Please run this script from the installation directory
    pause
    goto menu
)

echo.
echo Creating shortcut in Windows Startup folder...

timeout /t 1 >nul

REM Create a shortcut in the Startup folder
set "SHORTCUT_PATH=%STARTUP_DIR%\%SHORTCUT_NAME%"
set "TARGET_PATH=%SCRIPT_DIR%%BATCH_FILE%"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$WshShell=New-Object -ComObject WScript.Shell; $Shortcut=$WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath='%TARGET_PATH%'; $Shortcut.WorkingDirectory='%SCRIPT_DIR%'; $Shortcut.Description='Hydra Print Automation'; $Shortcut.Save()"

if %errorlevel% equ 0 (
    echo [SUCCESS] Added to Windows Startup
    echo The application will start automatically when you log in.
) else (
    echo [ERROR] Failed to create shortcut
)

pause
goto menu

:remove_startup
echo.
del "%STARTUP_DIR%\%SHORTCUT_NAME%" >nul 2>&1
if exist "%STARTUP_DIR%\%SHORTCUT_NAME%" (
    echo [ERROR] Failed to remove from Windows Startup
) else (
    echo [SUCCESS] Removed from Windows Startup
)
pause
goto menu

:end
exit /b 0
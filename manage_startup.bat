@echo off
setlocal enabledelayedexpansion

:: Hydra Print Automation
:: This script manages the Windows startup configuration for the Hydra Print Automation service

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    set "IS_ADMIN=1"
) else (
    set "IS_ADMIN=0"
)

REM Set paths and configuration
set "VERSION=1.3.0"
set "SCRIPT_DIR=%~dp0"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_NAME=HydraPrintAutomation.lnk"
set "TARGET_PATH=%SCRIPT_DIR%start_app.bat"

:menu
cls
echo =======================================
echo  Hydra Print Automation - Startup Manager
echo =======================================
echo 1. Add to Windows Startup
if %IS_ADMIN%==1 (
    echo 2. Remove from Windows Startup
    echo 3. Install as Windows Service (Admin)
    echo 4. Uninstall Windows Service (Admin)
    echo 5. Exit
) else (
    echo 2. Remove from Windows Startup
    echo 3. Exit
)
echo.
set "choice="
set /p "choice=Choose an option: "

if "%choice%"=="" goto menu
if "%choice%"=="1" goto add_startup
if "%choice%"=="2" goto remove_startup
if %IS_ADMIN%==1 if "%choice%"=="3" goto install_service
if %IS_ADMIN%==1 if "%choice%"=="4" goto uninstall_service
if %IS_ADMIN%==1 if "%choice%"=="5" goto end
if %IS_ADMIN%==0 if "%choice%"=="3" goto end
goto menu

:add_startup
if not exist "%TARGET_PATH%" (
    echo.
    echo [ERROR] Could not find start_app.bat in the current directory
    echo Please run this script from the installation directory
    pause
    goto menu
)

echo.
echo Adding to Windows Startup...

timeout /t 1 >nul

REM Create a shortcut in the Startup folder
powershell -NoProfile -ExecutionPolicy Bypass -Command "
try {
    $WshShell = New-Object -comObject WScript.Shell;
    $Shortcut = $WshShell.CreateShortcut('!STARTUP_DIR!\!SHORTCUT_NAME!');
    $Shortcut.TargetPath = '!TARGET_PATH!';
    $Shortcut.WorkingDirectory = '!SCRIPT_DIR!';
    $Shortcut.Description = 'Starts Hydra Print Automation v%VERSION% on login';
    $Shortcut.Save();
    Write-Host '[SUCCESS] Added to Windows Startup';
    Write-Host 'The application will start automatically when you log in.';
} catch {
    Write-Host '[ERROR] Failed to add to Windows Startup: ' $_.Exception.Message -ForegroundColor Red;
}"

pause
goto menu

:remove_startup
echo.
if exist "%STARTUP_DIR%\%SHORTCUT_NAME%" (
    echo Removing from Windows Startup...
    del "%STARTUP_DIR%\%SHORTCUT_NAME%"
    if errorlevel 1 (
        echo [ERROR] Failed to remove from Windows Startup
    ) else (
        echo [SUCCESS] Removed from Windows Startup
    )
) else (
    echo [INFO] No startup entry found
)
pause
goto menu

:install_service
if not exist "%SCRIPT_DIR%service_install.bat" (
    echo.
    echo [ERROR] Could not find service_install.bat
    pause
    goto menu
)

echo.
echo Installing Windows Service...
call "%SCRIPT_DIR%service_install.bat"
pause
goto menu

:uninstall_service
if not exist "%SCRIPT_DIR%service_uninstall.bat" (
    echo.
    echo [ERROR] Could not find service_uninstall.bat
    pause
    goto menu
)

echo.
echo Uninstalling Windows Service...
call "%SCRIPT_DIR%service_uninstall.bat"
pause
goto menu
goto menu

:end
exit /b 0

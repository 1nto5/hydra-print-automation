@echo off
echo Starting Hydra Print Automation Installation...

REM Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies from local deps folder
echo Installing dependencies...
pip install --no-index --find-links=./deps -r requirements.txt

REM Create necessary directories
if not exist logs mkdir logs

echo Installation completed successfully.
echo.
echo To run the application manually:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the application: python main.py
echo.
echo To install as a Windows service (requires administrator privileges):
echo 1. Run service_install.bat as administrator
echo.
pause 
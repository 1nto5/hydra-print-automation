@echo off
echo Starting Hydra Print Automation Installation...

REM Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies from local folder
echo Installing dependencies...
pip install --no-index --find-links=./packages -r requirements.txt

REM Set up environment variables
set API_TOKEN=your_token_here

REM Start the application
echo Starting the application...
python main.py

pause 
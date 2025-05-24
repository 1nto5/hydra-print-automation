@echo off
REM Install all dependencies from the local 'deps' folder
pip install --no-index --find-links=deps -r requirements.txt
echo Installation completed.
pause

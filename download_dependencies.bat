@echo off
REM Download all dependencies for offline use
python -m pip install --upgrade pip
pip download -r requirements.txt -d deps
echo Dependencies downloaded to the 'deps' folder.
pause

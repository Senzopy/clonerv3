@echo off
SETLOCAL

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

REM Start the Python script
echo Starting the script....
python main.py

REM Keep the console open in case of an error
echo.
echo Press any key to exit...
pause >nul

ENDLOCAL

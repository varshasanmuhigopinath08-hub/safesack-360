@echo off
title SafeSack 360
echo ========================================================
echo         SafeSack 360 - Hazard-Detection System
echo ========================================================
echo.

IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [1/3] Creating Python Virtual Environment (venv)...
    python -m venv venv
)

echo [2/3] Activating virtual environment & installing requirements...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo [3/3] Initializing database and running seed...
python seed.py

echo.
echo ========================================================
echo  Starting SafeSack 360 Web Application on http://0.0.0.0:5000
echo  Press Ctrl+C to stop.
echo ========================================================
echo.
python app.py
pause

@echo off
echo ========================================
echo iPSC Tracker - Server Production Launch
echo ========================================
echo.

cd /d "U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker"

echo Current directory: %CD%
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
python -c "import streamlit, pandas, openpyxl, pyperclip; print('✅ All dependencies available')" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo.
echo Starting iPSC Tracker on server...
echo Access URL: http://localhost:8501
echo Network URL: http://%COMPUTERNAME%:8501
echo.
echo Press Ctrl+C to stop the server
echo.

python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0

pause
@echo off
color 0E
title iPSC Tracker - Diagnostic Launcher
cls

echo ===============================================
echo  iPSC Tracker - Diagnostic Startup
echo ===============================================
echo.

cd /d "U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker"
echo Current directory: %CD%
echo.

echo Testing Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo ✅ Python OK
echo.

echo Testing Streamlit...
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
if errorlevel 1 (
    echo ERROR: Streamlit not installed!
    echo Installing...
    pip install streamlit
)
echo ✅ Streamlit OK
echo.

echo Testing database...
python -c "from db import get_conn; print('Database connection: OK')"
if errorlevel 1 (
    echo ERROR: Database connection failed!
    pause
    exit /b 1
)
echo ✅ Database OK
echo.

echo Testing for running instances...
netstat -an | findstr ":8501 "
if not errorlevel 1 (
    echo ⚠️ Port 8501 is already in use!
    echo Trying alternative port 8502...
    set PORT=8502
) else (
    echo ✅ Port 8501 is available
    set PORT=8501
)
echo.

echo Starting iPSC Tracker on port %PORT%...
echo.
echo Access URLs:
echo • Local:   http://localhost:%PORT%
echo • Network: http://%COMPUTERNAME%:%PORT%
echo.
echo Starting browser in 5 seconds...
echo Press Ctrl+C to cancel
timeout /t 5 /nobreak

start "" "http://localhost:%PORT%"

echo.
echo ===============================================
echo  Starting Streamlit Application...
echo ===============================================
python -m streamlit run app.py --server.port %PORT% --server.address 0.0.0.0 --server.headless true

echo.
echo Application stopped.
pause
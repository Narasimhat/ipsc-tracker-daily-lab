@echo off
title iPSC Tracker - Quick Launch
color 0A
echo.
echo ========================================
echo       iPSC Tracker Quick Launch
echo ========================================
echo.
echo Starting server and opening browser...
echo.

REM Start the server in background
start "iPSC Server" /min cmd /c "cd /d c:\Users\ntelugu\Desktop\2025_Python_Blockchain && python -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --browser.gatherUsageStats=false"

REM Wait a moment for server to start
timeout /t 5 /nobreak >nul

REM Open browser
start http://localhost:8501

echo ✅ iPSC Tracker started!
echo ✅ Browser opened
echo.
echo The server is running in a minimized window.
echo Close that window to stop the server.
echo.
pause
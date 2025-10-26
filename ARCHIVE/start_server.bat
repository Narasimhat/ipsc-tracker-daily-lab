@echo off
title iPSC Tracker Server
color 0A
echo.
echo ========================================
echo       iPSC Tracker Lab Server
echo ========================================
echo.
echo Stopping any existing servers...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo.
echo Starting iPSC Tracker...
echo.
echo Your iPSC Tracker will be available at:
echo   Local:   http://localhost:8501
echo   Network: http://10.84.128.4:8501
echo.
echo Keep this window open to keep the server running.
echo Press Ctrl+C to stop the server.
echo.
cd /d "c:\Users\ntelugu\Desktop\2025_Python_Blockchain"
python -m streamlit run app.py
echo.
echo Server stopped.
pause

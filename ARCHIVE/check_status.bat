@echo off
title iPSC Tracker Status Checker
color 0B
echo.
echo ========================================
echo     iPSC Tracker Status Check
echo ========================================
echo.

echo Checking if iPSC Tracker is running...
netstat -ano | findstr ":8501" >nul 2>&1

if %ERRORLEVEL% == 0 (
    echo ✅ iPSC Tracker is RUNNING
    echo.
    echo Access URLs:
    echo   Local:   http://localhost:8501
    echo   Network: http://10.84.128.4:8501
    echo.
    echo The server is ready for use!
) else (
    echo ❌ iPSC Tracker is NOT running
    echo.
    echo To start the server:
    echo 1. Double-click "start_server.bat"
    echo 2. Or use the desktop shortcut
    echo.
)

echo.
echo Current Python processes:
tasklist | findstr python.exe

echo.
pause
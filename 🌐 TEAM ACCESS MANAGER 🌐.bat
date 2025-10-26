@echo off
color 0C
title iPSC Tracker - Team Access Manager
cls

echo.
echo    ████████╗███████╗ █████╗ ███╗   ███╗     █████╗  ██████╗ ██████╗███████╗███████╗███████╗
echo    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║    ██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝
echo       ██║   █████╗  ███████║██╔████╔██║    ███████║██║     ██║     █████╗  ███████╗███████╗
echo       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║    ██╔══██║██║     ██║     ██╔══╝  ╚════██║╚════██║
echo       ██║   ███████╗██║  ██║██║ ╚═╝ ██║    ██║  ██║╚██████╗╚██████╗███████╗███████║███████║
echo       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝╚══════╝╚══════╝╚══════╝
echo.
echo    ══════════════════════════════════════════════════════════════════════════════════════
echo                              🌐 Team Access Manager 🌐
echo    ══════════════════════════════════════════════════════════════════════════════════════
echo.

set "SERVER_PATH=U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker"
cd /d "%SERVER_PATH%"

echo    🔍 Checking for existing iPSC Tracker instances...
echo.

REM Check for running instances
netstat -an | findstr ":8501 " >nul
if not errorlevel 1 (
    echo    ✅ iPSC Tracker is ALREADY RUNNING on port 8501
    echo       📱 Access URL: http://localhost:8501
    echo       🌐 Network URL: http://%COMPUTERNAME%:8501
    echo.
    echo    💡 No need to start another instance!
    echo       Just open your browser to the URL above.
    echo.
    goto EXISTING_INSTANCE
)

netstat -an | findstr ":8502 " >nul
if not errorlevel 1 (
    echo    ✅ iPSC Tracker is ALREADY RUNNING on port 8502
    echo       📱 Access URL: http://localhost:8502
    echo       🌐 Network URL: http://%COMPUTERNAME%:8502
    echo.
    echo    💡 No need to start another instance!
    echo       Just open your browser to the URL above.
    echo.
    goto EXISTING_INSTANCE
)

netstat -an | findstr ":8503 " >nul
if not errorlevel 1 (
    echo    ✅ iPSC Tracker is ALREADY RUNNING on port 8503
    echo       📱 Access URL: http://localhost:8503
    echo       🌐 Network URL: http://%COMPUTERNAME%:8503
    echo.
    echo    💡 No need to start another instance!
    echo       Just open your browser to the URL above.
    echo.
    goto EXISTING_INSTANCE
)

netstat -an | findstr ":8504 " >nul
if not errorlevel 1 (
    echo    ✅ iPSC Tracker is ALREADY RUNNING on port 8504
    echo       📱 Access URL: http://localhost:8504
    echo       🌐 Network URL: http://%COMPUTERNAME%:8504
    echo.
    echo    💡 No need to start another instance!
    echo       Just open your browser to the URL above.
    echo.
    goto EXISTING_INSTANCE
)

REM No instance found
echo    ❌ No iPSC Tracker instance found running
echo.
echo    🎯 Options:
echo       [1] Start new server instance (if you are the designated server manager)
echo       [2] Check network computers for running instances
echo       [3] Exit (someone else should start the server)
echo.

set /p CHOICE="    Select option (1-3): "

if "%CHOICE%"=="1" goto START_SERVER
if "%CHOICE%"=="2" goto NETWORK_CHECK
if "%CHOICE%"=="3" goto EXIT
goto ASK_CHOICE

:START_SERVER
echo.
echo    🚀 Starting new iPSC Tracker instance...
echo    ⚠️  You are now the SERVER MANAGER for this session!
echo    💡 Keep this window open while others use the application.
echo.
echo    ═══════════════════════════════════════════════════════════════
echo    📋 Share these URLs with your team:
echo       • Local:   http://localhost:8501
echo       • Network: http://%COMPUTERNAME%:8501
echo    ═══════════════════════════════════════════════════════════════
echo.

timeout /t 3 /nobreak >nul
start "" "http://localhost:8501"

python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true

echo.
echo    🛑 iPSC Tracker server stopped
echo    💡 Team members can no longer access the application
pause
goto EXIT

:EXISTING_INSTANCE
echo    ═══════════════════════════════════════════════════════════════
echo    🎯 What would you like to do?
echo    ═══════════════════════════════════════════════════════════════
echo.
echo    [1] Open iPSC Tracker in browser (recommended)
echo    [2] Show server details
echo    [3] Exit
echo.

set /p ACTION="    Select option (1-3): "

if "%ACTION%"=="1" goto OPEN_BROWSER
if "%ACTION%"=="2" goto SERVER_DETAILS
if "%ACTION%"=="3" goto EXIT
goto EXISTING_INSTANCE

:OPEN_BROWSER
echo.
echo    🌐 Opening iPSC Tracker in your browser...

REM Try to detect which port is running
netstat -an | findstr ":8501 " >nul
if not errorlevel 1 (
    start "" "http://localhost:8501"
    goto EXIT
)

netstat -an | findstr ":8502 " >nul
if not errorlevel 1 (
    start "" "http://localhost:8502"
    goto EXIT
)

netstat -an | findstr ":8503 " >nul
if not errorlevel 1 (
    start "" "http://localhost:8503"
    goto EXIT
)

netstat -an | findstr ":8504 " >nul
if not errorlevel 1 (
    start "" "http://localhost:8504"
    goto EXIT
)

echo    ❌ Could not detect running port automatically
echo    💡 Try opening http://localhost:8501 manually
pause
goto EXIT

:SERVER_DETAILS
echo.
echo    📊 Server Status Details:
echo    ════════════════════════════
echo    Computer Name: %COMPUTERNAME%
echo    Server Path: %SERVER_PATH%
echo    
for /f "tokens=2" %%i in ('netstat -an ^| findstr ":850"') do (
    echo    Active Port: %%i
)
echo.
echo    🌐 Team Access URLs:
echo       • http://%COMPUTERNAME%:8501
echo       • http://%COMPUTERNAME%:8502
echo       • http://%COMPUTERNAME%:8503
echo       • http://%COMPUTERNAME%:8504
echo.
pause
goto EXISTING_INSTANCE

:NETWORK_CHECK
echo.
echo    🔍 Network Instance Detection Guide:
echo    ═══════════════════════════════════════
echo.
echo    💡 To check if someone else is running the server:
echo.
echo    1. Ask team members if they started the server
echo    2. Try these common URLs in your browser:
echo       • http://[COLLEAGUE-COMPUTER]:8501
echo       • http://[SERVER-COMPUTER]:8501
echo.
echo    3. Check your lab's shared documentation for server info
echo.
echo    💡 If no server is running, designate someone to start it!
echo.
pause
goto EXIT

:EXIT
echo.
echo    👋 Team Access Manager closing
echo.
echo    💡 Remember: Only ONE server instance should run at a time!
echo    💡 Everyone else uses browsers to connect to that instance.
pause
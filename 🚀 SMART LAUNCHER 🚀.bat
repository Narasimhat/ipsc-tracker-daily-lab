@echo off
color 0A
title iPSC Tracker - Smart Launcher
cls

echo.
echo    ██╗██████╗ ███████╗ ██████╗    ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
echo    ██║██╔══██╗██╔════╝██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
echo    ██║██████╔╝███████╗██║            ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
echo    ██║██╔═══╝ ╚════██║██║            ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
echo    ██║██║     ███████║╚██████╗       ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
echo    ╚═╝╚═╝     ╚══════╝ ╚═════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
echo.
echo    ═══════════════════════════════════════════════════════════════════════════════════════
echo                             🧬 Laboratory Information Management System 🧬
echo    ═══════════════════════════════════════════════════════════════════════════════════════
echo.

set "SERVER_PATH=U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker"
cd /d "%SERVER_PATH%"

echo    🔍 Checking system requirements...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo    ❌ ERROR: Python not found!
    pause
    exit /b 1
)
echo    ✅ Python installation verified

echo    🗄️  Testing database connection...
python -c "from db import get_conn; get_conn()" >nul 2>&1
if errorlevel 1 (
    color 0C
    echo    ❌ Database connection failed!
    pause
    exit /b 1
)
echo    ✅ Database accessible

echo    🌐 Finding available port...

REM Check for available port starting from 8501
set PORT=8501
:CHECKPORT
netstat -an | findstr ":%PORT% " >nul 2>&1
if not errorlevel 1 (
    echo    ⚠️ Port %PORT% is busy, trying next...
    set /a PORT+=1
    if %PORT% GTR 8510 (
        echo    ❌ No available ports found in range 8501-8510
        pause
        exit /b 1
    )
    goto CHECKPORT
)

echo    ✅ Found available port: %PORT%
echo.
echo    🚀 Starting iPSC Tracker on port %PORT%...
echo    ⏳ Please wait while the application loads...
echo.
echo    📱 Access URLs:
echo       • Local:   http://localhost:%PORT%
echo       • Network: http://%COMPUTERNAME%:%PORT%
echo.
echo    💡 Opening browser automatically in 3 seconds...
echo    💡 Press Ctrl+C in this window to stop the server
echo.

timeout /t 3 /nobreak >nul
start "" "http://localhost:%PORT%"

echo    ═══════════════════════════════════════════════════════════════════════════════════════

python -m streamlit run app.py --server.port %PORT% --server.address 0.0.0.0 --server.headless true

echo.
echo    ═══════════════════════════════════════════════════════════════════════════════════════
echo    🛑 iPSC Tracker server stopped
echo    ═══════════════════════════════════════════════════════════════════════════════════════
pause
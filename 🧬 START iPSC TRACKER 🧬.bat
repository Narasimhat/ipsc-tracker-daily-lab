@echo off
color 0A
title iPSC Tracker - Laboratory Information Management System
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
echo    📍 Server Location: U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker
echo    🌐 Network Access: Available for team collaboration
echo    ✨ Features: Enhanced filtering, Lab book formatting, Clipboard functionality
echo.
echo    ═══════════════════════════════════════════════════════════════════════════════════════
echo.

set "SERVER_PATH=U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker"
cd /d "%SERVER_PATH%"

echo    🔍 Checking system requirements...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo    ❌ ERROR: Python not found!
    echo    📥 Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)
echo    ✅ Python installation verified

echo    📦 Verifying dependencies...
python -c "import streamlit, pandas, openpyxl, pyperclip" >nul 2>&1
if errorlevel 1 (
    echo    📥 Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        color 0C
        echo    ❌ Failed to install dependencies!
        pause
        exit /b 1
    )
)
echo    ✅ All dependencies ready

echo    🗄️  Testing database connection...
python -c "from db import get_conn; get_conn()" >nul 2>&1
if errorlevel 1 (
    color 0C
    echo    ❌ Database connection failed!
    pause
    exit /b 1
)
echo    ✅ Database accessible

echo.
echo    🚀 Starting iPSC Tracker Server...
echo    ⏳ Please wait while the application loads (30-45 seconds)...
echo.
echo    📱 Access URLs:
echo       • Local:   http://localhost:8501
echo       • Network: http://%COMPUTERNAME%:8501
echo.
echo    💡 Tips:
echo       • Set your name in "My name" field for personal filtering
echo       • Use "My entries only" to see just your data
echo       • Format entries for lab book using 🎨 Format button
echo       • Press Ctrl+C in this window to stop the server
echo.
echo    ═══════════════════════════════════════════════════════════════════════════════════════

timeout /t 3 /nobreak >nul
start "" "http://localhost:8501"

python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true

echo.
echo    ═══════════════════════════════════════════════════════════════════════════════════════
echo    🛑 iPSC Tracker server stopped
echo    ═══════════════════════════════════════════════════════════════════════════════════════
pause
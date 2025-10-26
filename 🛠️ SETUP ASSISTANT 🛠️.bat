@echo off
color 0B
title iPSC Tracker - Setup Assistant
cls

echo.
echo    ██╗██████╗ ███████╗ ██████╗    ███████╗███████╗████████╗██╗   ██╗██████╗ 
echo    ██║██╔══██╗██╔════╝██╔════╝    ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
echo    ██║██████╔╝███████╗██║         ███████╗█████╗     ██║   ██║   ██║██████╔╝
echo    ██║██╔═══╝ ╚════██║██║         ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ 
echo    ██║██║     ███████║╚██████╗    ███████║███████╗   ██║   ╚██████╔╝██║     
echo    ╚═╝╚═╝     ╚══════╝ ╚═════╝    ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     
echo.
echo    ═══════════════════════════════════════════════════════════════════════════
echo                               🛠️ System Setup Assistant 🛠️
echo    ═══════════════════════════════════════════════════════════════════════════
echo.

set "SERVER_PATH=U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker"
cd /d "%SERVER_PATH%"

echo    🔍 Checking system requirements...
echo.

REM Check Python
echo    [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ Python not found!
    echo.
    echo    📋 Python Installation Options:
    echo       1. Download from python.org (recommended)
    echo       2. Install from Microsoft Store
    echo       3. Use company software center
    echo.
    echo    🎯 Recommended Versions:
    echo       • Python 3.11.x (best stability)
    echo       • Python 3.12.x (latest stable)
    echo       • Minimum: Python 3.8+
    echo.
    echo    🔗 Quick links:
    echo       • Python.org: https://www.python.org/downloads/
    echo       • Microsoft Store: Search "Python" in Windows Store
    echo.
    echo    ⚠️  After installing Python, restart this launcher.
    echo.
    pause
    
    REM Try to open Python download page
    set /p OPENSITE="    💡 Open Python download page? (y/n): "
    if /i "%OPENSITE%"=="y" (
        start "" "https://www.python.org/downloads/"
    )
    
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo    ✅ Found: %PYTHON_VERSION%
    
    REM Check Python version compatibility
    for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do set VERSION_NUM=%%a
    for /f "tokens=1,2 delims=." %%a in ("%VERSION_NUM%") do (
        set MAJOR=%%a
        set MINOR=%%b
    )
    
    if %MAJOR% LSS 3 (
        echo    ⚠️  WARNING: Python 2 detected! Please upgrade to Python 3.8+
        pause
    ) else if %MAJOR% EQU 3 if %MINOR% LSS 8 (
        echo    ⚠️  WARNING: Python %VERSION_NUM% is below minimum requirement (3.8+)
        echo    💡 Consider upgrading for better compatibility
        pause
    ) else if %MAJOR% EQU 3 if %MINOR% GTR 12 (
        echo    ⚠️  INFO: Python %VERSION_NUM% is very new - compatibility unknown
        echo    💡 Consider using Python 3.11 or 3.12 if issues occur
    ) else (
        echo    ✅ Version is compatible
    )
)

REM Check Streamlit
echo    [2/4] Checking Streamlit...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo    ❌ Streamlit not installed
    echo    🔧 Installing Streamlit automatically...
    python -m pip install streamlit
    if errorlevel 1 (
        echo    ❌ Failed to install Streamlit
        echo    💡 Try running as administrator or check internet connection
        pause
        exit /b 1
    )
    echo    ✅ Streamlit installed successfully
) else (
    echo    ✅ Streamlit available
)

REM Check additional packages
echo    [3/4] Checking required packages...
python -c "import pandas, openpyxl, pyperclip" >nul 2>&1
if errorlevel 1 (
    echo    ⚠️  Some packages missing, installing...
    python -m pip install pandas openpyxl pyperclip
    if errorlevel 1 (
        echo    ❌ Failed to install packages
        pause
        exit /b 1
    )
    echo    ✅ All packages installed
) else (
    echo    ✅ All packages available
)

REM Check database
echo    [4/4] Checking database connection...
python -c "from db import get_conn; get_conn()" >nul 2>&1
if errorlevel 1 (
    echo    ❌ Database connection failed
    echo    💡 Check if database file exists and is accessible
    pause
    exit /b 1
) else (
    echo    ✅ Database connection OK
)

echo.
echo    ═══════════════════════════════════════════════════════════════════════════
echo    🎉 Setup Complete! All requirements satisfied.
echo    ═══════════════════════════════════════════════════════════════════════════
echo.
echo    🚀 Ready to launch iPSC Tracker!
echo.
set /p LAUNCH="    Launch application now? (y/n): "
if /i "%LAUNCH%"=="y" (
    echo    🔄 Starting Smart Launcher...
    call "🚀 SMART LAUNCHER 🚀.bat"
) else (
    echo    💡 Use '🚀 SMART LAUNCHER 🚀.bat' when ready to start
    pause
)
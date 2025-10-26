@echo off
color 0D
title iPSC Tracker - Version Upgrade Helper
cls

echo.
echo    ██╗   ██╗██████╗  ██████╗ ██████╗  █████╗ ██████╗ ███████╗
echo    ██║   ██║██╔══██╗██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔════╝
echo    ██║   ██║██████╔╝██║  ███╗██████╔╝███████║██║  ██║█████╗  
echo    ██║   ██║██╔═══╝ ██║   ██║██╔══██╗██╔══██║██║  ██║██╔══╝  
echo    ╚██████╔╝██║     ╚██████╔╝██║  ██║██║  ██║██████╔╝███████╗
echo     ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝
echo.
echo    ═══════════════════════════════════════════════════════════════
echo                      🔄 Python Version Upgrade Helper 🔄
echo    ═══════════════════════════════════════════════════════════════
echo.

set "SERVER_PATH=U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker"
cd /d "%SERVER_PATH%"

echo    This tool helps manage Python version upgrades for iPSC Tracker
echo.

REM Check current Python version
echo    📊 Current System Status:
echo    ════════════════════════════
python --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ Python: Not found
    echo    💡 Use Setup Assistant to install Python first
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo    ✅ Python: %%i
)

REM Check package status
echo    📦 Package Status:
python -c "import streamlit; print('   ✅ Streamlit:', streamlit.__version__)" 2>nul || echo    ❌ Streamlit: Not installed
python -c "import pandas; print('   ✅ Pandas:', pandas.__version__)" 2>nul || echo    ❌ Pandas: Not installed
python -c "import openpyxl; print('   ✅ OpenPyXL:', openpyxl.__version__)" 2>nul || echo    ❌ OpenPyXL: Not installed
python -c "import pyperclip; print('   ✅ Pyperclip: Available')" 2>nul || echo    ❌ Pyperclip: Not installed

echo.
echo    ═══════════════════════════════════════════════════════════════
echo    🎯 Upgrade Options:
echo    ═══════════════════════════════════════════════════════════════
echo.
echo    [1] Pre-upgrade backup (Save current package list)
echo    [2] Post-upgrade repair (Reinstall packages after Python upgrade)
echo    [3] Full diagnostic (Check all components)
echo    [4] Package cleanup (Remove and reinstall all packages)
echo    [5] Version compatibility check
echo    [6] Exit
echo.

set /p CHOICE="    Select option (1-6): "

if "%CHOICE%"=="1" goto BACKUP
if "%CHOICE%"=="2" goto REPAIR
if "%CHOICE%"=="3" goto DIAGNOSTIC
if "%CHOICE%"=="4" goto CLEANUP
if "%CHOICE%"=="5" goto COMPATIBILITY
if "%CHOICE%"=="6" goto EXIT
goto MENU

:BACKUP
echo.
echo    💾 Creating backup of current configuration...
echo    ════════════════════════════════════════════════
python --version > python_backup.txt 2>&1
pip list > packages_backup.txt 2>&1
echo    ✅ Current Python version saved to: python_backup.txt
echo    ✅ Current packages saved to: packages_backup.txt
echo.
echo    💡 After upgrading Python, run option [2] to restore packages
pause
goto MENU

:REPAIR
echo.
echo    🔧 Post-upgrade repair: Reinstalling packages...
echo    ════════════════════════════════════════════════
echo    📦 Installing required packages...
python -m pip install --upgrade pip
python -m pip install streamlit>=1.24 pandas>=1.5 pillow>=10 openpyxl>=3.0 matplotlib>=3.5 pyperclip>=1.8.2
if errorlevel 1 (
    echo    ❌ Package installation failed
    echo    💡 Try running as administrator or check internet connection
    pause
    goto MENU
)
echo    ✅ Package installation complete
echo.
echo    🧪 Testing application...
python -c "from db import get_conn; get_conn()" >nul 2>&1
if errorlevel 1 (
    echo    ❌ Database connection test failed
) else (
    echo    ✅ Database connection OK
)
echo.
echo    🎉 Repair complete! Try launching the application.
pause
goto MENU

:DIAGNOSTIC
echo.
echo    🔍 Running full diagnostic...
echo    ════════════════════════════
call "🔧 DIAGNOSTIC LAUNCHER 🔧.bat"
goto MENU

:CLEANUP
echo.
echo    🧹 Package cleanup: Remove and reinstall all packages...
echo    ════════════════════════════════════════════════════════
echo    ⚠️  This will remove and reinstall all Python packages
set /p CONFIRM="    Continue? (y/n): "
if /i not "%CONFIRM%"=="y" goto MENU

echo    🗑️  Uninstalling packages...
pip uninstall -y streamlit pandas pillow openpyxl matplotlib pyperclip
echo    📦 Reinstalling packages...
pip install streamlit>=1.24 pandas>=1.5 pillow>=10 openpyxl>=3.0 matplotlib>=3.5 pyperclip>=1.8.2
echo    ✅ Cleanup complete
pause
goto MENU

:COMPATIBILITY
echo.
echo    📊 Version Compatibility Check:
echo    ═══════════════════════════════
for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do set VERSION_NUM=%%a
echo    Current Python: %VERSION_NUM%
echo.
echo    ✅ Supported versions:
echo       • Python 3.8.x - Minimum supported
echo       • Python 3.9.x - Fully tested
echo       • Python 3.10.x - Corporate environments
echo       • Python 3.11.x - Recommended (best balance)
echo       • Python 3.12.x - Latest stable
echo.
echo    ⚠️  Avoid:
echo       • Python 3.7 and below - Not supported
echo       • Python 3.13+ beta - Wait for stable release
echo.

REM Parse version and give specific advice
for /f "tokens=1,2 delims=." %%a in ("%VERSION_NUM%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo    ❌ CRITICAL: Python 2 detected! Must upgrade to Python 3.8+
) else if %MAJOR% EQU 3 if %MINOR% LSS 8 (
    echo    ❌ WARNING: Python %VERSION_NUM% below minimum (3.8+) - upgrade recommended
) else if %MAJOR% EQU 3 if %MINOR% LEQ 12 (
    echo    ✅ GOOD: Python %VERSION_NUM% is fully supported
) else (
    echo    ⚠️  INFO: Python %VERSION_NUM% is very new - may have compatibility issues
)

pause
goto MENU

:MENU
echo.
echo    ═══════════════════════════════════════════════════════════════
echo    🎯 Upgrade Options:
echo    ═══════════════════════════════════════════════════════════════
echo.
echo    [1] Pre-upgrade backup (Save current package list)
echo    [2] Post-upgrade repair (Reinstall packages after Python upgrade)
echo    [3] Full diagnostic (Check all components)
echo    [4] Package cleanup (Remove and reinstall all packages)
echo    [5] Version compatibility check
echo    [6] Exit
echo.

set /p CHOICE="    Select option (1-6): "

:EXIT
echo.
echo    👋 Exiting upgrade helper
echo    💡 Use Setup Assistant for fresh installations
pause
@echo off
REM Test script to manually run the daily export
REM Use this to test the automation before setting up the scheduled task

echo ========================================
echo    Testing Daily Excel Export
echo ========================================

echo 🧪 This will test the daily export functionality...
echo.

REM Change to script directory
cd /d "%~dp0"

echo 📂 Current directory: %CD%
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python is available
echo.

REM Check if required files exist
if not exist "daily_excel_export.py" (
    echo ❌ daily_excel_export.py not found!
    pause
    exit /b 1
)

if not exist "db.py" (
    echo ❌ db.py not found!
    pause
    exit /b 1
)

echo ✅ Required files found
echo.

REM Run the test export
echo 🚀 Running test export...
echo.
python daily_excel_export.py

REM Check results
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Test export completed successfully!
    echo.
    echo 📁 Check the 'daily_exports' folder for the exported file
    echo 📋 Check 'daily_export_log.txt' for the export log
    echo.
    echo 🎯 The automation is working correctly!
    echo You can now set up the scheduled task using setup_daily_automation.ps1
) else (
    echo.
    echo ❌ Test export failed!
    echo Please check the error messages above and fix any issues.
)

echo.
pause
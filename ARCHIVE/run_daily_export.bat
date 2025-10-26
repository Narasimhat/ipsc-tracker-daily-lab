@echo off
REM Daily Excel Export Batch Script for iPSC Tracker
REM This script runs the Python automation script

echo ========================================
echo      iPSC Tracker - Daily Export
echo ========================================

REM Change to the script directory
cd /d "%~dp0"

REM Run the Python export script
echo Starting daily Excel export...
python daily_excel_export.py

REM Check if the export was successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Daily export completed successfully!
) else (
    echo.
    echo ❌ Daily export failed with error code %ERRORLEVEL%
)

echo.
echo Export log available in: daily_export_log.txt
echo Exported files stored in: daily_exports\

REM Keep window open for 10 seconds if run manually
timeout /t 10 /nobreak >nul 2>&1

exit /b %ERRORLEVEL%
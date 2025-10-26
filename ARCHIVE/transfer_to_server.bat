@echo off
echo ========================================
echo iPSC Tracker - Quick Server Transfer
echo ========================================
echo.

set SOURCE_PATH=C:\Users\ntelugu\Desktop\2025_Python_Blockchain
set SERVER_PATH=U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker

echo Source: %SOURCE_PATH%
echo Target: %SERVER_PATH%
echo.

echo Checking server accessibility...
if not exist "U:\AG_Diecke\DATA MANAGMENT\NT_Literature\" (
    echo ERROR: Server path not accessible!
    echo Please ensure U: drive is mounted
    pause
    exit /b 1
)

echo Creating server directory...
if not exist "%SERVER_PATH%" mkdir "%SERVER_PATH%"

echo Copying project files...
xcopy "%SOURCE_PATH%\*" "%SERVER_PATH%\" /E /I /H /Y /EXCLUDE:transfer_exclude.txt

echo.
echo ========================================
echo Transfer completed!
echo ========================================
echo.
echo Server location: %SERVER_PATH%
echo.
echo Next steps:
echo 1. Navigate to the server folder
echo 2. Install dependencies: pip install -r requirements.txt
echo 3. Run the application: python -m streamlit run app.py
echo.
pause
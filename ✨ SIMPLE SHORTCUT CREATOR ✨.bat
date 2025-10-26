@echo off
echo Creating desktop shortcut for iPSC Tracker...

set "TARGET=U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker\🧬 START iPSC TRACKER 🧬.bat"
set "SHORTCUT=%USERPROFILE%\Desktop\🧬 iPSC Tracker - Lab Management.lnk"

powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%TARGET%'; $Shortcut.WorkingDirectory = 'U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker'; $Shortcut.Description = 'iPSC Tracker - Laboratory Information Management System'; $Shortcut.Save()"

if exist "%SHORTCUT%" (
    echo ✅ Desktop shortcut created successfully!
    echo 📱 Look for: 🧬 iPSC Tracker - Lab Management
    echo 🎯 Double-click to start the application
) else (
    echo ❌ Failed to create shortcut
)

echo.
pause
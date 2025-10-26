# Create Desktop Shortcut for iPSC Tracker
# Run this once to create a desktop shortcut

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$AppPath = "c:\Users\ntelugu\Desktop\2025_Python_Blockchain"
$ShortcutPath = "$DesktopPath\iPSC Tracker.lnk"

$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "$AppPath\start_server.bat"
$Shortcut.WorkingDirectory = $AppPath
$Shortcut.Description = "iPSC Tracker Lab Server - One Click Start"
$Shortcut.IconLocation = "$AppPath\start_server.bat,0"
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created: iPSC Tracker.lnk"
Write-Host ""
Write-Host "🎯 How to use:"
Write-Host "1. Double-click 'iPSC Tracker' on your desktop"
Write-Host "2. Wait for the server to start"
Write-Host "3. Open http://localhost:8080 in your browser"
Write-Host "4. Keep the black window open while using the app"
Write-Host "5. Close the black window to stop the server"
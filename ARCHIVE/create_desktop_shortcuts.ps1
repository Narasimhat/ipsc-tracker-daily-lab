# iPSC Tracker - Desktop Shortcut Creator for Team
# Creates attractive desktop shortcuts for all team members

param(
    [string]$UserName = $env:USERNAME,
    [switch]$AllUsers = $false
)

# Configuration
$AppName = "🧬 iPSC Tracker - Lab Management"
$ServerPath = "U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker"
$LauncherFile = "🧬 START iPSC TRACKER 🧬.bat"

Write-Host "🧬 iPSC Tracker - Desktop Shortcut Creator 🧬" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green
Write-Host ""

function Create-Shortcut {
    param(
        [string]$TargetPath,
        [string]$ShortcutPath,
        [string]$Description
    )
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        $Shortcut.TargetPath = $TargetPath
        $Shortcut.WorkingDirectory = Split-Path $TargetPath
        $Shortcut.Description = $Description
        $Shortcut.WindowStyle = 1  # Normal window
        $Shortcut.Save()
        
        # Release COM object
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($Shortcut) | Out-Null
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($WshShell) | Out-Null
        
        return $true
    } catch {
        Write-Host "❌ Error creating shortcut: $_" -ForegroundColor Red
        return $false
    }
}

# Check if server path exists
if (!(Test-Path $ServerPath)) {
    Write-Host "❌ Server path not found: $ServerPath" -ForegroundColor Red
    pause
    exit 1
}

# Check if launcher file exists
$LauncherPath = Join-Path $ServerPath $LauncherFile
if (!(Test-Path $LauncherPath)) {
    Write-Host "❌ Launcher file not found: $LauncherPath" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "✅ iPSC Tracker installation verified" -ForegroundColor Green

# Determine desktop path
if ($AllUsers) {
    $DesktopPath = [Environment]::GetFolderPath("CommonDesktopDirectory")
    Write-Host "🌐 Creating shortcut for all users" -ForegroundColor Cyan
} else {
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    Write-Host "👤 Creating shortcut for user: $UserName" -ForegroundColor Cyan
}

$ShortcutPath = Join-Path $DesktopPath "$AppName.lnk"

Write-Host "🔧 Creating desktop shortcut..." -ForegroundColor Yellow

$shortcutCreated = Create-Shortcut -TargetPath $LauncherPath -ShortcutPath $ShortcutPath -Description "iPSC Tracker - Laboratory Information Management System"

if ($shortcutCreated) {
    Write-Host "✅ Desktop shortcut created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Team Instructions:" -ForegroundColor Yellow
    Write-Host "   1. Double-click: $AppName" -ForegroundColor White
    Write-Host "   2. Wait for startup (30-45 seconds)" -ForegroundColor White
    Write-Host "   3. Browser opens automatically" -ForegroundColor White
    Write-Host "   4. Set your name and start tracking!" -ForegroundColor White
    Write-Host ""
    Write-Host "🎉 Ready to use!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create shortcut" -ForegroundColor Red
}

pause
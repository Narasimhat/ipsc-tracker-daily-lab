# PowerShell Script to Setup Windows Task Scheduler for Daily Excel Export
# Run this script as Administrator to set up automatic daily exports

param(
    [Parameter(Mandatory=$false)]
    [string]$Time = "09:00",  # Default time: 9:00 AM
    
    [Parameter(Mandatory=$false)]
    [string]$TaskName = "iPSC_Tracker_Daily_Export"
)

Write-Host "========================================" -ForegroundColor Green
Write-Host "   iPSC Tracker - Automation Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Get the current script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BatchFile = Join-Path $ScriptDir "run_daily_export.bat"

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "❌ This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and 'Run as Administrator', then run this script again." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "📂 Script directory: $ScriptDir" -ForegroundColor Cyan
Write-Host "🕒 Scheduled time: $Time daily" -ForegroundColor Cyan
Write-Host "📝 Task name: $TaskName" -ForegroundColor Cyan
Write-Host ""

# Check if batch file exists
if (-not (Test-Path $BatchFile)) {
    Write-Host "❌ Batch file not found: $BatchFile" -ForegroundColor Red
    exit 1
}

try {
    # Delete existing task if it exists
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "🗑️  Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Create the scheduled task action
    $Action = New-ScheduledTaskAction -Execute $BatchFile -WorkingDirectory $ScriptDir

    # Create the scheduled task trigger (daily at specified time)
    $Trigger = New-ScheduledTaskTrigger -Daily -At $Time

    # Create task settings
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    # Create the principal (run as SYSTEM or current user)
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType ServiceAccount

    # Register the scheduled task
    Write-Host "📅 Creating scheduled task..." -ForegroundColor Green
    
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Daily Excel export for iPSC Tracker database" -Force

    Write-Host "✅ Task successfully created!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName" -ForegroundColor White
    Write-Host "  Schedule: Daily at $Time" -ForegroundColor White
    Write-Host "  Action: $BatchFile" -ForegroundColor White
    Write-Host "  Working Directory: $ScriptDir" -ForegroundColor White
    Write-Host ""

    # Test the task
    Write-Host "🧪 Testing the task (this may take a moment)..." -ForegroundColor Yellow
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 5

    # Check task status
    $TaskInfo = Get-ScheduledTask -TaskName $TaskName
    Write-Host "📊 Task Status: $($TaskInfo.State)" -ForegroundColor Cyan

    Write-Host ""
    Write-Host "🎯 Setup Complete!" -ForegroundColor Green
    Write-Host "Your iPSC Tracker will now automatically export to Excel every day at $Time" -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 Export files will be saved to: $ScriptDir\daily_exports\" -ForegroundColor Cyan
    Write-Host "📋 Export log will be saved to: $ScriptDir\daily_export_log.txt" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚙️  To modify or remove this task:" -ForegroundColor Yellow
    Write-Host "  1. Open Task Scheduler (taskschd.msc)" -ForegroundColor White
    Write-Host "  2. Find '$TaskName' in Task Scheduler Library" -ForegroundColor White
    Write-Host "  3. Right-click to modify, disable, or delete" -ForegroundColor White

} catch {
    Write-Host "❌ Error creating scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
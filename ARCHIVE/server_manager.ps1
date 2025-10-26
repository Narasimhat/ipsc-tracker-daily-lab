# iPSC Tracker Server Startup Script
# Run this as Administrator to start the service

param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "start"
)

$AppPath = "c:\Users\ntelugu\Desktop\2025_Python_Blockchain"
$LogFile = "$AppPath\server.log"
$PidFile = "$AppPath\server.pid"

function Start-iPSCServer {
    Write-Host "Starting iPSC Tracker Server..."
    
    # Kill any existing processes
    Stop-iPSCServer -Silent
    
    # Start the server
    $Process = Start-Process -FilePath "python" -ArgumentList "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true" -WorkingDirectory $AppPath -PassThru -RedirectStandardOutput $LogFile -RedirectStandardError $LogFile
    
    # Save process ID
    $Process.Id | Out-File -FilePath $PidFile
    
    Write-Host "iPSC Tracker started on http://localhost:8501"
    Write-Host "Process ID: $($Process.Id)"
    Write-Host "Log file: $LogFile"
    
    # Show network IP for lab access
    $NetworkIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"}).IPAddress[0]
    Write-Host "Lab Network Access: http://$NetworkIP:8501"
}

function Stop-iPSCServer {
    param([switch]$Silent)
    
    if (Test-Path $PidFile) {
        $ProcessId = Get-Content $PidFile
        try {
            Stop-Process -Id $ProcessId -Force
            if (!$Silent) { Write-Host "Stopped iPSC Tracker (PID: $ProcessId)" }
        } catch {
            if (!$Silent) { Write-Host "Process $ProcessId not found or already stopped" }
        }
        Remove-Item $PidFile -ErrorAction SilentlyContinue
    }
    
    # Also kill any streamlit processes
    Get-Process | Where-Object {$_.ProcessName -like "*python*" -and $_.CommandLine -like "*streamlit*"} | Stop-Process -Force -ErrorAction SilentlyContinue
}

function Get-iPSCStatus {
    if (Test-Path $PidFile) {
        $ProcessId = Get-Content $PidFile
        $Process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
        if ($Process) {
            Write-Host "iPSC Tracker is RUNNING (PID: $ProcessId)"
            Write-Host "Started: $($Process.StartTime)"
            
            $NetworkIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"}).IPAddress[0]
            Write-Host "Access URLs:"
            Write-Host "  Local: http://localhost:8501"
            Write-Host "  Network: http://$NetworkIP:8501"
        } else {
            Write-Host "iPSC Tracker is STOPPED (stale PID file)"
            Remove-Item $PidFile -ErrorAction SilentlyContinue
        }
    } else {
        Write-Host "iPSC Tracker is STOPPED"
    }
}

# Main execution
switch ($Action.ToLower()) {
    "start" { Start-iPSCServer }
    "stop" { Stop-iPSCServer }
    "restart" { 
        Stop-iPSCServer
        Start-Sleep -Seconds 2
        Start-iPSCServer 
    }
    "status" { Get-iPSCStatus }
    default {
        Write-Host "Usage: .\server_manager.ps1 [start|stop|restart|status]"
        Write-Host ""
        Write-Host "Examples:"
        Write-Host "  .\server_manager.ps1 start    # Start the server"
        Write-Host "  .\server_manager.ps1 stop     # Stop the server"
        Write-Host "  .\server_manager.ps1 status   # Check if running"
    }
}
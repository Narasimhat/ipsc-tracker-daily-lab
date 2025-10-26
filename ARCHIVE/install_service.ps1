# Install iPSC Tracker as Windows Service
# Run as Administrator

param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "install"
)

$ServiceName = "iPSCTracker"
$ServiceDisplayName = "iPSC Tracker Lab Server"
$ServiceDescription = "Laboratory Information Management System for iPSC culture tracking"
$AppPath = "c:\Users\ntelugu\Desktop\2025_Python_Blockchain"
$PythonPath = (Get-Command python).Source
$StartupScript = "$AppPath\service_wrapper.py"

# Create service wrapper script
$WrapperContent = @"
import subprocess
import sys
import os
import time

def run_streamlit():
    os.chdir(r'$AppPath')
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.address=0.0.0.0',
        '--server.port=8080',
        '--server.headless=true'
    ]
    
    while True:
        try:
            process = subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"Streamlit crashed: {e}")
            print("Restarting in 5 seconds...")
            time.sleep(5)

if __name__ == '__main__':
    run_streamlit()
"@

$WrapperContent | Out-File -FilePath $StartupScript -Encoding UTF8

function Install-Service {
    Write-Host "Installing iPSC Tracker as Windows Service..."
    
    # Use NSSM (Non-Sucking Service Manager) - more reliable than sc.exe for Python apps
    $nssmPath = "$AppPath\nssm.exe"
    
    if (!(Test-Path $nssmPath)) {
        Write-Host "Downloading NSSM (service manager)..."
        $nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
        $nssmZip = "$AppPath\nssm.zip"
        
        Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
        Expand-Archive -Path $nssmZip -DestinationPath $AppPath
        Copy-Item "$AppPath\nssm-2.24\win64\nssm.exe" $nssmPath
        Remove-Item $nssmZip, "$AppPath\nssm-2.24" -Recurse
    }
    
    # Install service
    & $nssmPath install $ServiceName $PythonPath $StartupScript
    & $nssmPath set $ServiceName DisplayName $ServiceDisplayName
    & $nssmPath set $ServiceName Description $ServiceDescription
    & $nssmPath set $ServiceName Start SERVICE_AUTO_START
    
    # Set working directory
    & $nssmPath set $ServiceName AppDirectory $AppPath
    
    # Set log files
    & $nssmPath set $ServiceName AppStdout "$AppPath\service_output.log"
    & $nssmPath set $ServiceName AppStderr "$AppPath\service_error.log"
    
    Write-Host "Service installed successfully!"
    Write-Host "Starting service..."
    Start-Service $ServiceName
    
    Write-Host "iPSC Tracker is now running as a Windows Service"
    Write-Host "It will automatically start when the computer boots"
}

function Remove-Service {
    Write-Host "Removing iPSC Tracker service..."
    Stop-Service $ServiceName -ErrorAction SilentlyContinue
    & "$AppPath\nssm.exe" remove $ServiceName confirm
    Write-Host "Service removed"
}

function Get-ServiceStatus {
    $Service = Get-Service $ServiceName -ErrorAction SilentlyContinue
    if ($Service) {
        Write-Host "Service Status: $($Service.Status)"
        if ($Service.Status -eq "Running") {
            $NetworkIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"}).IPAddress[0]
            Write-Host "Access URLs:"
            Write-Host "  Local: http://localhost:8080"
            Write-Host "  Network: http://$NetworkIP:8080"
        }
    } else {
        Write-Host "Service not installed"
    }
}

# Main execution
switch ($Action.ToLower()) {
    "install" { Install-Service }
    "remove" { Remove-Service }
    "status" { Get-ServiceStatus }
    default {
        Write-Host "Usage: .\install_service.ps1 [install|remove|status]"
        Write-Host ""
        Write-Host "Examples:"
        Write-Host "  .\install_service.ps1 install  # Install as Windows service"
        Write-Host "  .\install_service.ps1 remove   # Remove service"
        Write-Host "  .\install_service.ps1 status   # Check service status"
    }
}
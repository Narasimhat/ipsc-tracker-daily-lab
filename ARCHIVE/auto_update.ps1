# Auto-update script for iPSC Tracker
# Schedule this to run daily via Task Scheduler

param(
    [Parameter(Mandatory=$false)]
    [string]$GitRepo = "https://github.com/your-username/ipsc-tracker.git",
    
    [Parameter(Mandatory=$false)]
    [string]$AppPath = "c:\Users\ntelugu\Desktop\2025_Python_Blockchain",
    
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

$LogFile = "$AppPath\update.log"

function Write-Log {
    param($Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$Timestamp - $Message" | Out-File -FilePath $LogFile -Append
    Write-Host "$Timestamp - $Message"
}

function Update-App {
    Write-Log "Starting auto-update check..."
    
    try {
        # Check if git repo
        if (!(Test-Path "$AppPath\.git")) {
            Write-Log "Not a git repository. Manual deployment detected."
            return
        }
        
        # Fetch latest changes
        Set-Location $AppPath
        git fetch origin
        
        # Check if updates available
        $LocalCommit = git rev-parse HEAD
        $RemoteCommit = git rev-parse origin/main
        
        if ($LocalCommit -eq $RemoteCommit -and !$Force) {
            Write-Log "No updates available."
            return
        }
        
        Write-Log "Updates found. Backing up current version..."
        
        # Create backup
        $BackupDir = "$AppPath\backups\pre-update-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        New-Item -ItemType Directory -Path $BackupDir -Force
        
        # Backup database and important files
        Copy-Item "$AppPath\ipsc_tracker.db" $BackupDir -ErrorAction SilentlyContinue
        Copy-Item "$AppPath\images" $BackupDir -Recurse -ErrorAction SilentlyContinue
        
        Write-Log "Stopping application..."
        & "$AppPath\server_manager.ps1" stop
        
        Write-Log "Pulling updates..."
        git pull origin main
        
        Write-Log "Installing dependencies..."
        pip install -r requirements.txt --upgrade
        
        Write-Log "Starting application..."
        & "$AppPath\server_manager.ps1" start
        
        Write-Log "Update completed successfully!"
        
    } catch {
        Write-Log "Error during update: $($_.Exception.Message)"
        Write-Log "Application may need manual restart"
    }
}

# Run update
Update-App
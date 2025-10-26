# iPSC Tracker - Server Transfer Script
# Transfers the project from local desktop to server location
# Target: U:\AG_Diecke\DATA MANAGMENT\NT_Literature

param(
    [string]$SourcePath = "C:\Users\ntelugu\Desktop\2025_Python_Blockchain",
    [string]$ServerPath = "U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker",
    [switch]$CreateBackup = $true,
    [switch]$PreserveLocal = $true
)

Write-Host "🚀 iPSC Tracker - Server Transfer Script" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Function to check if path exists and is accessible
function Test-PathAccess {
    param([string]$Path)
    try {
        if (Test-Path $Path) {
            return $true
        } else {
            return $false
        }
    } catch {
        return $false
    }
}

# Function to copy files with progress
function Copy-ProjectFiles {
    param(
        [string]$Source,
        [string]$Destination,
        [string[]]$ExcludePatterns = @()
    )
    
    Write-Host "📂 Copying files from $Source to $Destination..." -ForegroundColor Yellow
    
    # Create destination directory if it doesn't exist
    if (!(Test-Path $Destination)) {
        New-Item -Path $Destination -ItemType Directory -Force | Out-Null
        Write-Host "✅ Created destination directory: $Destination" -ForegroundColor Green
    }
    
    # Define files/folders to exclude
    $defaultExcludes = @(
        "__pycache__",
        ".venv",
        "*.pyc",
        ".git",
        "node_modules",
        "server.pid"
    )
    
    $allExcludes = $defaultExcludes + $ExcludePatterns
    
    # Copy files using robocopy for better handling
    $robocopyArgs = @(
        $Source,
        $Destination,
        "/MIR",  # Mirror directory tree
        "/R:3",  # Retry 3 times on failed copies
        "/W:5",  # Wait 5 seconds between retries
        "/MT:8", # Multi-threaded copy
        "/XD"    # Exclude directories
    )
    
    # Add excluded directories
    foreach ($exclude in $allExcludes) {
        $robocopyArgs += $exclude
    }
    
    Write-Host "🔄 Starting file transfer..." -ForegroundColor Cyan
    & robocopy @robocopyArgs
    
    if ($LASTEXITCODE -le 7) {  # Robocopy exit codes 0-7 are success
        Write-Host "✅ File transfer completed successfully!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ File transfer failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        return $false
    }
}

# Function to create backup
function Create-Backup {
    param([string]$ServerPath)
    
    if (Test-Path $ServerPath) {
        $backupPath = "$ServerPath" + "_backup_" + (Get-Date -Format "yyyyMMdd_HHmmss")
        Write-Host "💾 Creating backup at: $backupPath" -ForegroundColor Yellow
        
        try {
            Copy-Item -Path $ServerPath -Destination $backupPath -Recurse -Force
            Write-Host "✅ Backup created successfully!" -ForegroundColor Green
            return $backupPath
        } catch {
            Write-Host "❌ Backup creation failed: $_" -ForegroundColor Red
            return $null
        }
    } else {
        Write-Host "ℹ️ No existing installation found - no backup needed" -ForegroundColor Cyan
        return "none"
    }
}

# Function to update paths in configuration files
function Update-ConfigPaths {
    param([string]$ServerPath)
    
    Write-Host "⚙️ Updating configuration files for server environment..." -ForegroundColor Yellow
    
    # Update start_server.bat to use server paths
    $startServerPath = Join-Path $ServerPath "start_server.bat"
    if (Test-Path $startServerPath) {
        $content = Get-Content $startServerPath -Raw
        $content = $content -replace "C:\\Users\\ntelugu\\Desktop\\2025_Python_Blockchain", $ServerPath
        Set-Content -Path $startServerPath -Value $content
        Write-Host "✅ Updated start_server.bat paths" -ForegroundColor Green
    }
    
    # Update daily export paths
    $dailyExportPath = Join-Path $ServerPath "daily_excel_export.py"
    if (Test-Path $dailyExportPath) {
        $content = Get-Content $dailyExportPath -Raw
        $content = $content -replace "C:\\Users\\ntelugu\\Desktop\\2025_Python_Blockchain", $ServerPath
        Set-Content -Path $dailyExportPath -Value $content
        Write-Host "✅ Updated daily_excel_export.py paths" -ForegroundColor Green
    }
    
    # Create server-specific launch script
    $serverLaunchScript = @"
@echo off
echo Starting iPSC Tracker on Server...
cd /d "$ServerPath"
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
pause
"@
    
    $serverLaunchPath = Join-Path $ServerPath "start_server_production.bat"
    Set-Content -Path $serverLaunchPath -Value $serverLaunchScript
    Write-Host "✅ Created server production launch script" -ForegroundColor Green
}

# Function to verify server installation
function Test-ServerInstallation {
    param([string]$ServerPath)
    
    Write-Host "🔍 Verifying server installation..." -ForegroundColor Yellow
    
    $requiredFiles = @(
        "app.py",
        "db.py",
        "requirements.txt",
        "README.md"
    )
    
    $allPresent = $true
    foreach ($file in $requiredFiles) {
        $filePath = Join-Path $ServerPath $file
        if (Test-Path $filePath) {
            Write-Host "✅ Found: $file" -ForegroundColor Green
        } else {
            Write-Host "❌ Missing: $file" -ForegroundColor Red
            $allPresent = $false
        }
    }
    
    return $allPresent
}

# Main execution
Write-Host "📋 Transfer Configuration:" -ForegroundColor Cyan
Write-Host "   Source: $SourcePath" -ForegroundColor White
Write-Host "   Target: $ServerPath" -ForegroundColor White
Write-Host "   Create Backup: $CreateBackup" -ForegroundColor White
Write-Host "   Preserve Local: $PreserveLocal" -ForegroundColor White
Write-Host ""

# Step 1: Verify source path
if (!(Test-PathAccess $SourcePath)) {
    Write-Host "❌ Source path not accessible: $SourcePath" -ForegroundColor Red
    exit 1
}

# Step 2: Verify server path accessibility
$serverRoot = "U:\AG_Diecke\DATA MANAGMENT\NT_Literature"
if (!(Test-PathAccess $serverRoot)) {
    Write-Host "❌ Server root path not accessible: $serverRoot" -ForegroundColor Red
    Write-Host "   Please ensure the network drive is mounted and accessible" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Source and server paths are accessible" -ForegroundColor Green

# Step 3: Create backup if requested and needed
if ($CreateBackup) {
    $backupResult = Create-Backup -ServerPath $ServerPath
    if ($backupResult -eq $null) {
        Write-Host "❌ Backup creation failed. Aborting transfer." -ForegroundColor Red
        exit 1
    }
}

# Step 4: Transfer files
$transferSuccess = Copy-ProjectFiles -Source $SourcePath -Destination $ServerPath

if (!$transferSuccess) {
    Write-Host "❌ File transfer failed. Aborting." -ForegroundColor Red
    exit 1
}

# Step 5: Update configuration files
Update-ConfigPaths -ServerPath $ServerPath

# Step 6: Verify installation
$verificationSuccess = Test-ServerInstallation -ServerPath $ServerPath

if ($verificationSuccess) {
    Write-Host ""
    Write-Host "🎉 Server Transfer Completed Successfully!" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host "📍 Server Location: $ServerPath" -ForegroundColor Cyan
    Write-Host "🚀 To start the server application:" -ForegroundColor Yellow
    Write-Host "   1. Navigate to: $ServerPath" -ForegroundColor White
    Write-Host "   2. Run: start_server_production.bat" -ForegroundColor White
    Write-Host ""
    Write-Host "📝 Next Steps:" -ForegroundColor Yellow
    Write-Host "   • Install Python dependencies: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "   • Test the application: python -m streamlit run app.py" -ForegroundColor White
    Write-Host "   • Set up daily automation on server if needed" -ForegroundColor White
    
    if ($PreserveLocal) {
        Write-Host ""
        Write-Host "💾 Local copy preserved at: $SourcePath" -ForegroundColor Cyan
    }
} else {
    Write-Host "❌ Installation verification failed!" -ForegroundColor Red
    exit 1
}
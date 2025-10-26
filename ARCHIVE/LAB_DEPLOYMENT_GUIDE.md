# Lab Network Setup Guide for iPSC Tracker

## 🖥️ Server Setup (Windows Lab Computer)

### 1. Prepare the Lab Server
```powershell
# Run as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Navigate to app directory
cd "c:\Users\ntelugu\Desktop\2025_Python_Blockchain"

# Start the server
.\server_manager.ps1 start
```

### 2. Configure Windows Firewall
```powershell
# Allow incoming connections on port 8080
New-NetFirewallRule -DisplayName "iPSC Tracker" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
```

### 3. Set Static IP (Recommended)
- Go to Network Settings → Change adapter options
- Right-click your network connection → Properties
- Select "Internet Protocol Version 4 (TCP/IPv4)" → Properties
- Set static IP (e.g., 192.168.1.100)
- Note: Coordinate with your IT department

## 📱 Lab Access Setup

### Find Your Lab Server IP:
```powershell
# Get server IP address
ipconfig | findstr IPv4
```

### Access URLs:
- **Server local**: http://localhost:8080
- **Lab network**: http://[SERVER_IP]:8080
- **Example**: http://192.168.1.100:8080

## 🔄 Auto-Start Options

### Option A: Simple Startup (Easy)
1. Create shortcut to `start_server.bat`
2. Place in Windows Startup folder:
   ```
   Windows + R → shell:startup → OK
   ```
3. Copy shortcut there

### Option B: Windows Service (Recommended)
```powershell
# Run as Administrator
.\install_service.ps1 install
```

### Option C: Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: "When computer starts"
4. Action: Start program
5. Program: `powershell.exe`
6. Arguments: `-File "C:\path\to\server_manager.ps1" start`

## 🔧 Automatic Updates

### Setup Daily Updates:
```powershell
# Create scheduled task for auto-updates
schtasks /create /tn "iPSC Tracker Update" /tr "powershell.exe -File 'C:\path\to\auto_update.ps1'" /sc daily /st 02:00 /ru SYSTEM
```

## 🏥 Lab Network Best Practices

### 1. Server Requirements:
- **Minimum**: 4GB RAM, 50GB storage
- **Recommended**: 8GB RAM, 100GB storage
- **OS**: Windows 10/11 Pro (for better network features)

### 2. Network Security:
- Use strong passwords for user accounts
- Consider VPN access for remote work
- Regular database backups
- Keep Windows updated

### 3. Multi-User Setup:
- Each lab member creates their operator profile in Settings
- Shared database ensures everyone sees same data
- Images stored centrally on server

### 4. Backup Strategy:
```powershell
# Manual backup (run weekly)
.\server_manager.ps1 status
# Then use Settings tab → Backup Database

# Automated backups via Task Scheduler
schtasks /create /tn "iPSC Backup" /tr "powershell.exe -File 'C:\path\to\backup_script.ps1'" /sc weekly /d SUN /st 01:00
```

## 📊 Data Persistence

### Database Location:
- **File**: `ipsc_tracker.db` (SQLite)
- **Images**: `images/` folder
- **Backups**: `backups/` folder

### Sync Across Devices:
1. **Network Drive**: Store app on shared network drive
2. **Git**: Version control for code, manual DB sync
3. **Cloud**: OneDrive/Google Drive for backups only

## 🔍 Monitoring & Maintenance

### Health Checks:
```powershell
# Check if running
.\server_manager.ps1 status

# View logs
Get-Content server.log -Tail 20

# Restart if needed
.\server_manager.ps1 restart
```

### Performance Optimization:
- Close unnecessary programs on server
- Schedule updates during off-hours
- Monitor disk space for images
- Regular database maintenance

## 🆘 Troubleshooting

### Common Issues:

**Can't Access from Other Computers:**
1. Check Windows Firewall
2. Verify server IP address
3. Ensure server is running on 0.0.0.0:8080

**App Won't Start:**
1. Check Python installation
2. Install missing packages: `pip install -r requirements.txt`
3. Check port conflicts: `netstat -ano | findstr 8080`

**Database Errors:**
1. Check disk space
2. Verify file permissions
3. Restore from backup if needed

**Performance Issues:**
1. Restart the server
2. Check available RAM
3. Reduce image upload sizes

### Getting Help:
- Check log files in app directory
- Contact IT for network issues
- Backup before making changes
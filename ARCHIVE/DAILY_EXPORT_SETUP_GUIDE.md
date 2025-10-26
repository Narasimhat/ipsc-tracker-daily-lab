# 📅 Daily Excel Export Automation Setup Guide

## 🎯 Overview
This automation system will automatically export your iPSC Tracker database to Excel every day at a specified time using Windows Task Scheduler.

## 📁 Files Created
- `daily_excel_export.py` - Main automation script
- `run_daily_export.bat` - Batch wrapper for the automation
- `setup_daily_automation.ps1` - PowerShell script to setup Windows Task Scheduler
- `test_daily_export.bat` - Test script to verify automation works
- `export_config.py` - Configuration settings

## 🚀 Quick Setup (3 Steps)

### Step 1: Test the Automation
```batch
# Double-click this file to test:
test_daily_export.bat
```
This will verify everything works before setting up the schedule.

### Step 2: Setup Automated Schedule
```powershell
# Right-click PowerShell -> "Run as Administrator", then run:
cd "C:\Users\ntelugu\Desktop\2025_Python_Blockchain"
.\setup_daily_automation.ps1
```

### Step 3: Verify Setup
- Open Task Scheduler (Start → Search "Task Scheduler")
- Look for "iPSC_Tracker_Daily_Export" in Task Scheduler Library
- Check that it's enabled and scheduled for your desired time

## ⚙️ Customization

### Change Export Time
Edit the setup script and change the time:
```powershell
.\setup_daily_automation.ps1 -Time "14:30"  # For 2:30 PM
```

### Change File Retention
Edit `export_config.py`:
```python
DAYS_TO_KEEP = 60  # Keep files for 60 days instead of 30
```

## 📂 Output Files

### Daily Exports
- **Location**: `daily_exports/` folder
- **Format**: `iPSC_Daily_Export_YYYYMMDD_HHMMSS.xlsx`
- **Content**: Complete database with all tables and data
- **Retention**: Automatically deleted after 30 days (configurable)

### Export Log
- **File**: `daily_export_log.txt`
- **Content**: 
  ```
  2025-10-26 09:00:15 - SUCCESS - daily_exports/iPSC_Daily_Export_20251026_090015.xlsx
  2025-10-27 09:00:12 - SUCCESS - daily_exports/iPSC_Daily_Export_20251027_090012.xlsx
  ```

## 🔧 Advanced Configuration

### Manual Export
Run anytime manually:
```batch
run_daily_export.bat
```

### Schedule Multiple Times
You can create multiple scheduled tasks for different times:
```powershell
.\setup_daily_automation.ps1 -Time "09:00" -TaskName "iPSC_Morning_Export"
.\setup_daily_automation.ps1 -Time "17:00" -TaskName "iPSC_Evening_Export"
```

### Custom Export Directory
Edit `daily_excel_export.py` line 25:
```python
exports_dir = "C:/Lab_Backups/iPSC_Exports"  # Custom path
```

## 🛠️ Troubleshooting

### Common Issues

**1. "Python not found" Error**
- Ensure Python is installed and in PATH
- Test: Open Command Prompt → Type `python --version`

**2. "Permission Denied" Error**
- Run PowerShell as Administrator for setup
- Ensure the script directory is writable

**3. "Database locked" Error**
- Make sure iPSC Tracker app is not running during export
- The automation handles this automatically

**4. Task Doesn't Run**
- Check Task Scheduler for error messages
- Verify the task is enabled
- Check that the user account has proper permissions

### Viewing Task Scheduler Logs
1. Open Task Scheduler
2. Find "iPSC_Tracker_Daily_Export"
3. Click "History" tab to see execution logs

### Manual Debugging
Run the Python script directly to see detailed error messages:
```batch
cd "C:\Users\ntelugu\Desktop\2025_Python_Blockchain"
python daily_excel_export.py
```

## 📋 Task Scheduler Details

### Task Properties
- **Name**: iPSC_Tracker_Daily_Export
- **Trigger**: Daily at specified time
- **Action**: Run `run_daily_export.bat`
- **Settings**: 
  - Run whether user is logged on or not
  - Run with highest privileges
  - Start when available

### Modifying the Schedule
1. Open Task Scheduler (Win+R → `taskschd.msc`)
2. Navigate to Task Scheduler Library
3. Right-click "iPSC_Tracker_Daily_Export"
4. Select "Properties"
5. Go to "Triggers" tab → Edit

## 🔄 Backup Strategy

### What Gets Backed Up
- ✅ All log entries with complete data
- ✅ Reference tables (cell lines, media, etc.)
- ✅ Experimental workflow data
- ✅ User and assignment information
- ✅ Metadata and timestamps

### What's NOT Backed Up
- ❌ Image files (optional: can be enabled in config)
- ❌ Application settings
- ❌ Temporary files

### Multiple Backup Locations
Consider setting up multiple export locations:
1. Local daily exports (current system)
2. Network drive copy (manual setup)
3. Cloud storage sync (OneDrive, Google Drive, etc.)

## 📞 Support

### Quick Fixes
- **Restart the Task**: Task Scheduler → Right-click task → "Run"
- **Recreate Task**: Run `setup_daily_automation.ps1` again
- **Manual Export**: Double-click `test_daily_export.bat`

### Getting Help
If you encounter issues:
1. Check `daily_export_log.txt` for error messages
2. Run `test_daily_export.bat` to identify problems
3. Verify Task Scheduler settings and permissions

---

## 🎉 Success!
Once set up, your iPSC Tracker database will automatically backup to Excel every day. You'll have:
- ✅ Automated daily backups
- ✅ 30-day file retention
- ✅ Complete export logs
- ✅ Easy manual override options
- ✅ Professional-grade backup system
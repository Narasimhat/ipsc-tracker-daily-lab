# iPSC Tracker - Server Installation Guide

## 🎯 Server Transfer Process

### **Target Location**
```
U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker\
```

### **Transfer Methods**

#### **Method 1: PowerShell Script (Recommended)**
```powershell
# Run from the current project directory
.\transfer_to_server.ps1
```

#### **Method 2: Simple Batch File**
```batch
# Double-click or run from command prompt
transfer_to_server.bat
```

#### **Method 3: Manual Copy**
1. Create folder: `U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker\`
2. Copy all files except: `__pycache__`, `.venv`, `server.pid`, `.git`
3. Update paths in configuration files

## 🔧 Server Setup Instructions

### **1. Verify Transfer**
Navigate to server location and check these files exist:
- ✅ `app.py` (main application)
- ✅ `db.py` (database functions)  
- ✅ `requirements.txt` (dependencies)
- ✅ `ipsc_tracker.db` (database file)
- ✅ `images/` (uploaded images folder)

### **2. Install Python Dependencies**
```bash
# Navigate to server folder
cd "U:\AG_Diecke\DATA MANAGMENT\NT_Literature\iPSC_Tracker"

# Install required packages
pip install -r requirements.txt
```

### **3. Test Installation**
```bash
# Test basic imports
python -c "import streamlit, pandas, openpyxl; print('✅ All dependencies installed')"

# Test database connection
python -c "from db import get_conn; print('✅ Database accessible')"
```

### **4. Launch Application**
```bash
# Method 1: Direct launch
python -m streamlit run app.py --server.port 8501

# Method 2: Use production launcher
start_server_production.bat
```

## 🌐 Server Access Configuration

### **Local Network Access**
Application will be available at:
- **Local**: `http://localhost:8501`
- **Network**: `http://[SERVER-IP]:8501`

### **Firewall Configuration**
Ensure port 8501 is open for team access:
```powershell
# Add firewall rule (run as administrator)
netsh advfirewall firewall add rule name="iPSC Tracker" dir=in action=allow protocol=TCP localport=8501
```

## 📊 Database Migration

### **Existing Data**
- ✅ Database file (`ipsc_tracker.db`) transferred with all existing entries
- ✅ Images folder transferred with all uploaded files
- ✅ Export history preserved in `daily_exports/` folder

### **Backup Strategy**
```batch
# Create backup before major changes
copy "ipsc_tracker.db" "ipsc_tracker_backup_YYYYMMDD.db"
```

## ⚙️ Daily Automation Setup (Optional)

### **Server-Based Daily Exports**
1. Update paths in `setup_daily_automation.ps1`
2. Run as administrator to create scheduled task
3. Exports will be saved to server location

### **Configuration Files Updated**
- `start_server.bat` → Updated paths for server environment
- `daily_excel_export.py` → Updated export paths
- `start_server_production.bat` → New production launcher

## 🔧 Troubleshooting

### **Common Issues**

#### **"Module not found" errors**
```bash
# Ensure all dependencies installed
pip install -r requirements.txt

# Check specific package
pip list | grep streamlit
```

#### **Database connection errors**
```bash
# Verify database file exists and is readable
python -c "import sqlite3; conn = sqlite3.connect('ipsc_tracker.db'); print('✅ Database OK')"
```

#### **Network access issues**
```bash
# Test with different address binding
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

#### **Permission errors**
- Ensure read/write access to server folder
- Check that database file is not read-only
- Verify images folder has write permissions

## 🎯 Team Access

### **User Instructions**
1. **Access URL**: `http://[SERVER-NAME]:8501`
2. **Set Name**: Use "My name" field for personal filtering
3. **Data Location**: All data stored on server for team sharing

### **Administrator Tasks**
- Monitor server performance
- Regular database backups
- User management in Settings tab
- System updates and maintenance

## 📈 Performance Monitoring

### **Server Resource Usage**
- **RAM**: ~100MB for typical usage
- **Storage**: Database grows ~1MB per 1000 entries
- **Network**: Minimal bandwidth for web interface

### **Maintenance Schedule**
- **Daily**: Automated Excel exports (if configured)
- **Weekly**: Check disk space and logs
- **Monthly**: Database backup and cleanup
- **Quarterly**: Update dependencies and review security

## ✅ Verification Checklist

After server setup, verify:
- [ ] Application launches without errors
- [ ] Database contains existing data
- [ ] All images display correctly
- [ ] Team members can access via network
- [ ] Copy-paste functionality works
- [ ] Excel exports function properly
- [ ] User filtering operates correctly
- [ ] Daily automation configured (if desired)

## 🆘 Support

For issues with server deployment:
1. Check this guide first
2. Review error messages in terminal
3. Verify file permissions and network access
4. Test with minimal configuration
5. Contact system administrator if needed
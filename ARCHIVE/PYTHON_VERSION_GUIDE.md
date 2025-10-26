# 🐍 Python Version Management for iPSC Tracker

## Current Requirements

### ✅ Supported Python Versions:
- **Python 3.8+** (minimum)
- **Python 3.9** - ✅ Fully tested
- **Python 3.10** - ✅ Fully tested  
- **Python 3.11** - ✅ Recommended
- **Python 3.12** - ✅ Latest stable
- **Python 3.13** - ⚠️ Should work (untested)

### 📦 Package Requirements:
```
streamlit>=1.24
pandas>=1.5
pillow>=10
openpyxl>=3.0
matplotlib>=3.5
pyperclip>=1.8.2
```

---

## 🔄 What Happens with Python Version Upgrades

### **Scenario 1: Minor Updates (e.g., 3.11.5 → 3.11.8)**
- ✅ **Usually seamless** - packages continue working
- ✅ **No action needed** - just restart the application
- ✅ **Existing packages preserved**

### **Scenario 2: Major Updates (e.g., 3.11 → 3.12)**
- ⚠️ **Packages may need reinstalling**
- ⚠️ **Virtual environments break**
- ⚠️ **May require package updates**

### **Scenario 3: Breaking Changes (e.g., 3.8 → 3.13)**
- ❌ **Major compatibility issues possible**
- ❌ **Package versions may be incompatible**
- ❌ **Code changes might be needed**

---

## 🛠️ Handling Version Upgrades

### **Before Upgrading Python:**

#### 1. Check Current Setup
```batch
python --version
pip list > current_packages.txt
```

#### 2. Test Compatibility
```batch
# Run diagnostic to ensure everything works
🔧 DIAGNOSTIC LAUNCHER 🔧.bat
```

#### 3. Backup Current Installation
- Save `current_packages.txt`
- Note current Python version
- Backup database if needed

### **After Upgrading Python:**

#### 1. Reinstall Packages
```batch
# Method 1: Use Setup Assistant (Recommended)
🛠️ SETUP ASSISTANT 🛠️.bat

# Method 2: Manual reinstall
pip install streamlit pandas pillow openpyxl matplotlib pyperclip
```

#### 2. Test Application
```batch
🔧 DIAGNOSTIC LAUNCHER 🔧.bat
```

#### 3. If Issues Occur
```batch
# Uninstall and reinstall packages
pip uninstall streamlit pandas pillow openpyxl matplotlib pyperclip
pip install streamlit pandas pillow openpyxl matplotlib pyperclip
```

---

## 🎯 Recommended Python Versions

### **For New Installations:**
- **Python 3.11.x** - Best stability/feature balance
- **Python 3.12.x** - Latest stable with all features

### **For Corporate Environments:**
- **Python 3.10.x** - Wide compatibility
- **Python 3.11.x** - Modern features, stable

### **To Avoid:**
- **Python 3.7 and below** - Not supported
- **Python 3.13 beta** - Wait for stable release

---

## 🚨 Troubleshooting Version Issues

### **Problem: "ModuleNotFoundError" after Python upgrade**
**Solution:**
```batch
# Reinstall all packages
🛠️ SETUP ASSISTANT 🛠️.bat
```

### **Problem: Streamlit won't start**
**Solution:**
```batch
# Force reinstall Streamlit
pip uninstall streamlit
pip install streamlit
```

### **Problem: Database connection fails**
**Solution:**
```batch
# Check database file exists
dir ipsc_tracker.db
# Test connection
python -c "from db import get_conn; print('DB OK')"
```

### **Problem: Multiple Python versions installed**
**Solution:**
```batch
# Check which Python is being used
where python
# Use specific version if needed
py -3.11 --version
```

---

## 🔧 Enhanced Setup Assistant

The **🛠️ SETUP ASSISTANT 🛠️.bat** now handles:

✅ **Version Detection** - Shows current Python version  
✅ **Compatibility Check** - Warns if version too old  
✅ **Package Verification** - Tests all required packages  
✅ **Auto-Installation** - Installs missing packages  
✅ **Version Recommendations** - Suggests optimal versions  

---

## 📋 Version Upgrade Checklist

### Before Upgrade:
- [ ] Run diagnostic launcher
- [ ] Note current Python version
- [ ] Save package list: `pip list > packages_backup.txt`
- [ ] Backup database if critical data

### After Upgrade:
- [ ] Run Setup Assistant
- [ ] Test application launch
- [ ] Verify all features work
- [ ] Check database connection
- [ ] Test lab book formatting
- [ ] Verify clipboard functionality

### If Problems:
- [ ] Run diagnostic launcher for errors
- [ ] Reinstall packages manually
- [ ] Check Python PATH
- [ ] Consider downgrading if critical issues

---

## 💡 Best Practices

1. **Don't upgrade Python during critical work periods**
2. **Test upgrades on a different computer first**
3. **Keep backup of working Python environment**
4. **Use Setup Assistant after any Python changes**
5. **Document working configurations for team**

---

*The iPSC Tracker is designed to be robust across Python versions, but following these guidelines ensures smooth operation during upgrades.*
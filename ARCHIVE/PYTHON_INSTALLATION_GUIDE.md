# 🐍 Python Installation Guide for iPSC Tracker

## If Python is Not Available

### ❌ What You'll See:
```
🔍 Checking system requirements...
❌ ERROR: Python not found!
```

### ✅ Solutions:

## Option 1: Microsoft Store (Easiest)
1. Open **Microsoft Store** 
2. Search for **"Python"**
3. Install **Python 3.12** (or latest version)
4. Restart the launcher

## Option 2: Python.org (Recommended)
1. Go to https://www.python.org/downloads/
2. Download **Python for Windows**
3. **Important**: Check ✅ "Add Python to PATH" during installation
4. Install with default settings
5. Restart the launcher

## Option 3: Company Software Center
1. Check your company's software center
2. Look for **Python** or **Anaconda**
3. Install according to company policies

## Option 4: Portable Python (If admin rights limited)
1. Download **WinPython** or **Anaconda Individual**
2. Extract to a folder you have write access to
3. Modify launcher to use specific Python path

---

## 🛠️ New Setup Assistant

Use the new **🛠️ SETUP ASSISTANT 🛠️.bat** file which will:

✅ **Check for Python** and guide installation if missing  
✅ **Auto-install Streamlit** and required packages  
✅ **Verify database** connection  
✅ **Launch application** when ready  

---

## 🚨 Troubleshooting

### "Python not found" even after installation:
- **Restart your computer** 
- **Restart Command Prompt/PowerShell**
- **Check PATH**: Open cmd and type `python --version`

### Installation blocked by company policy:
- Contact IT department
- Request Python installation
- Use **🛠️ SETUP ASSISTANT 🛠️.bat** to identify specific needs

### Alternative: Request IT to install:
```
Required software:
- Python 3.8+ 
- pip (usually included)
- Packages: streamlit, pandas, openpyxl, pyperclip
```

---

## 📞 Getting Help

1. **Try Setup Assistant first**: 🛠️ SETUP ASSISTANT 🛠️.bat
2. **Check with IT** if installation blocked
3. **Use Diagnostic Launcher** for detailed error info
4. **Contact system administrator** for corporate environments

---

*The iPSC Tracker needs Python to run the web interface and manage data. Once Python is installed, everything else can be automatically configured.*
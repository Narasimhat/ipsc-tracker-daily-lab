# 🌐 Team Usage Guide - Shared Server Access

## 🚨 IMPORTANT: Don't Start Multiple Instances!

### ❌ What NOT to Do:
- **Don't** let everyone click launchers
- **Don't** start multiple server instances
- **Don't** run on different ports simultaneously

### ✅ What TO Do:
- **One person** starts the server
- **Everyone else** uses browsers to connect
- **Use Team Access Manager** for coordination

---

## 🎯 Recommended Team Workflow

### **Step 1: Designate Server Manager**
Choose **ONE person** as the daily server manager:
- **Most reliable computer** in the lab
- **Present for most of the day**
- **Responsible** for starting/stopping server

### **Step 2: Server Manager Starts Application**
Server manager uses: **🌐 TEAM ACCESS MANAGER 🌐.bat**
- Checks for existing instances first
- Starts new instance only if needed
- Shows team access URLs

### **Step 3: Team Members Connect**
Everyone else:
1. **Open web browser**
2. **Go to**: `http://[SERVER-COMPUTER]:8501`
3. **Start working** - no software installation needed

---

## 🛠️ Using Team Access Manager

### **What It Does:**
✅ **Detects existing instances** - prevents duplicates  
✅ **Shows connection URLs** - easy team access  
✅ **Guides team coordination** - clear instructions  
✅ **Prevents conflicts** - smart instance management  

### **For Server Manager:**
```
🌐 TEAM ACCESS MANAGER 🌐.bat
→ No instance found → Option [1] Start server
→ Keep window open during lab hours
→ Share URLs with team
```

### **For Team Members:**
```
🌐 TEAM ACCESS MANAGER 🌐.bat  
→ Instance detected → Option [1] Open browser
→ Automatic connection to running instance
→ Start working immediately
```

---

## 📋 Team Coordination Protocol

### **Daily Startup:**
1. **First person in lab** becomes server manager
2. **Use Team Access Manager** to start server
3. **Share computer name** with team (e.g., "Server on COMPUTER-LAB-01")
4. **Post URLs** in team chat/whiteboard

### **During Day:**
- **Team members** use browsers only
- **Don't restart** server unless necessary
- **Refresh browser** to see others' updates
- **Set your name** in "My name" field for filtering

### **End of Day:**
- **Server manager** closes application (Ctrl+C)
- **Team members** can close browsers
- **Daily backup** recommended (Settings tab)

---

## 🌐 Network Access URLs

### **For Team Members:**
Replace `[COMPUTER-NAME]` with actual server computer name:

- **Primary**: `http://[COMPUTER-NAME]:8501`
- **Backup**: `http://[COMPUTER-NAME]:8502` (if port conflict)
- **Local** (server computer only): `http://localhost:8501`

### **Finding Computer Name:**
- **Windows**: Open Command Prompt → type `hostname`
- **Or**: Check computer name in System Properties
- **Or**: Use Team Access Manager - shows computer name

---

## 🚨 Troubleshooting Team Access

### **"Can't connect" errors:**
1. **Check if server is running** - ask server manager
2. **Try Team Access Manager** - detects running instances
3. **Check computer name** - use correct server computer
4. **Check firewall** - Windows may block connections

### **Multiple instances running:**
1. **Stop all instances** (Ctrl+C in all command windows)
2. **Wait 30 seconds** for ports to clear
3. **Designate one server manager**
4. **Start single instance** with Team Access Manager

### **Data not syncing:**
- **Manual refresh needed** - press F5 in browser
- **Check same server** - ensure everyone uses same URL
- **Restart browsers** if persistent issues

---

## 💡 Best Practices Summary

### **DO:**
✅ Use **🌐 TEAM ACCESS MANAGER 🌐.bat** for all access  
✅ Designate **one server manager** per day  
✅ Share **computer name/URLs** with team  
✅ Set **individual names** for personal filtering  
✅ **Refresh browsers** to see updates  
✅ **Daily backups** by server manager  

### **DON'T:**
❌ Let multiple people start servers  
❌ Use different launchers simultaneously  
❌ Run on multiple ports  
❌ Restart server unnecessarily  
❌ Forget to set your operator name  

---

## 📞 Quick Reference

### **I want to use iPSC Tracker:**
→ Use **🌐 TEAM ACCESS MANAGER 🌐.bat**

### **I'm the first person today:**
→ Team Access Manager → Option [1] Start server

### **Someone else started the server:**
→ Team Access Manager → Option [1] Open browser

### **Can't find the server:**
→ Team Access Manager → Option [2] Network check

### **Need to restart everything:**
→ Stop all instances → Wait → One person starts fresh

---

*The Team Access Manager ensures safe, coordinated access to the shared iPSC Tracker server!*
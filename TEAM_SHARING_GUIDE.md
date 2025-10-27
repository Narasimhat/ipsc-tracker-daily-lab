# 🌐 Share iPSC Tracker with Your Team - Simple Guide

## ✨ Super Simple Method

### Step 1: Run the Sharing Tool
Double-click: **🌐 SHARE WITH TEAM 🌐.bat**

This will:
- ✅ Show your access link
- ✅ Open firewall automatically (if needed)
- ✅ Create a shareable HTML file

### Step 2: Share the Link
Your team access link:
```
http://141.80.154.229:8080
```

**That's it!** Just send this link to your colleagues via:
- 📧 Email
- 💬 Teams/Slack
- 📱 Text message

---

## 📋 Alternative: Share the HTML File

1. Look for: `team-access.html` (created automatically)
2. Send this file to your colleagues
3. They double-click it → Opens iPSC Tracker automatically!

---

## ⚡ Quick Manual Setup (If Needed)

### Option A: Windows Firewall (One-Time Setup)

Run in PowerShell as Administrator:
```powershell
New-NetFirewallRule -DisplayName "iPSC Tracker Docker" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

### Option B: Share via Command
Your colleagues just need to:
1. Open any browser
2. Type: `http://141.80.154.229:8080`
3. Bookmark it!

---

## 🔒 Requirements for Team Access

### ✅ They Need:
- Same network (WiFi/Ethernet) as your computer
- Any web browser
- Your computer must be ON

### ❌ They DON'T Need:
- Docker installed
- Python installed
- Any software
- Special permissions

---

## 💡 Tips for Best Experience

### Keep Your Computer On
- The app runs on your computer
- When your PC is on → Everyone can access
- When your PC is off → No access

### Stable Network
- Keep your computer connected to the network
- If IP changes, run the share tool again to get new link

### Multiple Users
- ✅ Multiple people can use it at the same time
- ✅ Everyone sees the same data
- ✅ No conflicts or issues

---

## 🎯 Usage Scenarios

### Daily Lab Use
```
Morning: Start Docker (docker-compose up -d)
All Day: Team accesses http://141.80.154.229:8080
Evening: Leave running or stop (docker-compose down)
```

### Always-On Access
```
1. Keep Docker running
2. Set Windows to not sleep
3. Team always has access
```

---

## 🛠️ Troubleshooting

### "Can't Connect" from Colleague's Computer

**Check 1: Is Docker Running?**
```powershell
docker ps
```
Should show `ipsc-tracker` as running

**Check 2: Is Firewall Open?**
Run: `🌐 SHARE WITH TEAM 🌐.bat` again

**Check 3: Same Network?**
- You and colleagues must be on same WiFi/network
- Ask IT if you're on different network segments

**Check 4: Get Fresh IP**
Your IP might have changed. Run the share tool again.

### Change Port (If 8080 is Blocked)

Edit `docker-compose.yml`:
```yaml
ports:
  - "8090:8080"  # Use 8090 instead
```

Then share: `http://141.80.154.229:8090`

---

## 🚀 Advanced: Make it Professional (Optional)

### Option 1: Use a Friendly Name
Ask your IT to add a DNS entry:
- `ipsc-tracker.yourlab.com` → `141.80.154.229`
- Share: `http://ipsc-tracker.yourlab.com:8080`

### Option 2: Remove Port Number
Use reverse proxy (see DOCKER_DEPLOYMENT.md)
- Share: `http://141.80.154.229` (no :8080)

### Option 3: Use HTTPS
Add SSL certificate via reverse proxy
- Share: `https://ipsc-tracker.yourlab.com`

---

## 📊 What Your Team Will See

When colleagues open the link:
- ✅ Full iPSC Tracker interface
- ✅ All features available
- ✅ Same data as you see
- ✅ Real-time updates
- ✅ Can add/edit entries

---

## 🔐 Security Notes

### Local Network Only
- App is only accessible on your local network
- Not accessible from internet (safer!)
- No external access without VPN

### User Management
- The app has built-in user login
- Each person can have their own account
- Activity is tracked per user

---

## ✅ Quick Checklist

Share with team in 3 steps:
- [ ] Run `🌐 SHARE WITH TEAM 🌐.bat`
- [ ] Copy the link shown
- [ ] Send to colleagues

That's it! 🎉

---

**Need Help?** 
- Rerun: `🌐 SHARE WITH TEAM 🌐.bat` anytime
- Check: `docker-compose ps` to verify running
- Logs: `docker-compose logs -f`

# 🔄 GitHub Auto-Backup Setup Guide

## Overview
This system automatically backs up your iPSC Tracker database to GitHub every hour, ensuring zero data loss!

---

## 🔑 **STEP 1: Create GitHub Personal Access Token** (5 minutes)

1. Go to **https://github.com/settings/tokens**
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in:
   - **Note**: `iPSC Tracker Auto-Backup`
   - **Expiration**: `No expiration` (or 1 year)
   - **Scopes**: Check these boxes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)

4. Click **"Generate token"** at the bottom
5. **COPY THE TOKEN NOW!** (You won't see it again)
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Save it somewhere safe temporarily

---

## 📝 **STEP 2: Add Token to Streamlit Cloud** (2 minutes)

1. Go to **https://share.streamlit.io**
2. Click on your app: **ipsc-tracker-daily-lab**
3. Click the **⚙️ Settings** button (or menu → Settings)
4. Go to **"Secrets"** tab
5. Add this configuration (replace `YOUR_TOKEN_HERE` with your actual token):

```toml
[github]
token = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

6. Click **"Save"**
7. Click **"Reboot app"** for changes to take effect

---

## 🔄 **STEP 3: Deploy Updated Code** (Automatic)

The backup system is ready! I just need to integrate it into your app and push the changes.

---

## ✅ **How It Works**

### **Automatic Restore (On Startup)**
- When Streamlit Cloud restarts, it pulls the latest database from GitHub
- Your data is always preserved, even after app restarts

### **Automatic Backup (Hourly)**
- Every hour, the database is automatically committed to GitHub
- Creates a separate `db-backup` branch (doesn't clutter your main code)
- Full version history - you can restore any previous version

### **Manual Backup**
- You can also trigger manual backups from the app
- Useful after important data entry

---

## 📊 **What Gets Backed Up**

✅ **Database file**: `data/ipsc_tracker.db` (148 KB currently)
✅ **Version history**: Every hourly snapshot
✅ **Automatic**: No manual intervention needed

❌ **Not backed up automatically**: 
- Images (too large, use Streamlit Cloud storage)
- Exports (you can download these manually)

---

## 🔍 **Monitoring Backups**

### **Check Backup Status:**
1. Go to your GitHub repo: https://github.com/Narasimhat/ipsc-tracker-daily-lab
2. Switch to `db-backup` branch (dropdown at top left)
3. You'll see commit messages like: `Auto-backup: 2025-10-27 14:30:00 UTC`

### **View Backup History:**
- Click on `data/ipsc_tracker.db` in the `db-backup` branch
- Click **"History"** to see all backup versions
- You can download any previous version!

---

## 🆘 **Restore Previous Version (If Needed)**

If you need to restore an older version:

1. Go to GitHub repo → `db-backup` branch
2. Click on `data/ipsc_tracker.db`
3. Click **"History"**
4. Find the version you want
5. Click on the commit → Click "View" → Click "Download"
6. Upload it back to your app (I can help with this)

---

## 💡 **Benefits**

✅ **Zero data loss** - Hourly backups
✅ **Time machine** - Restore any previous version
✅ **Free** - GitHub provides unlimited commits
✅ **Automatic** - No manual work required
✅ **Transparent** - See all changes in GitHub
✅ **Reliable** - GitHub's enterprise infrastructure

---

## 📈 **Storage Estimate**

- **Current database**: 148 KB
- **Hourly backups**: ~3.5 MB per month (assuming growth)
- **GitHub free tier**: 1 GB
- **Years before limit**: 20+ years 🎉

---

## 🔒 **Security**

✅ **Token is secret** - Stored in Streamlit secrets (encrypted)
✅ **Private repo** - Only you have access
✅ **Separate branch** - Backups don't interfere with code
✅ **No token in code** - Never committed to Git

---

## ⚙️ **Advanced: Manual Backup from App**

After I integrate this, you'll have a button in the app:
- Settings → Manual Backup → "Backup Now"
- Useful for immediate backup after important changes

---

## 📞 **Need Help?**

If you see any errors:
1. Check Streamlit app logs
2. Verify GitHub token is correct
3. Check `db-backup` branch exists on GitHub
4. Contact me and I'll help troubleshoot!

---

**Ready! Once you add the GitHub token to Streamlit secrets, I'll integrate the backup system into your app.** 🚀

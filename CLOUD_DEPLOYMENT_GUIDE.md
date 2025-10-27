# 🌐 Cloud Deployment Guide - iPSC Tracker with Supabase

## 🎯 **Complete Professional Setup**

This guide will help you deploy iPSC Tracker to the cloud with a **persistent PostgreSQL database** using Supabase + Streamlit Cloud.

---

## 📋 **Prerequisites**
- GitHub account (you have this ✅)
- Supabase account (free - we'll create)
- Streamlit Cloud account (free - we'll create)
- ~30 minutes of your time

---

## 🚀 **Step-by-Step Deployment**

### **STEP 1: Create Supabase Project** (5 minutes)

1. Go to **https://supabase.com**
2. Click **"Start your project"**
3. Sign in with GitHub
4. Click **"New project"**
5. Fill in:
   - **Name**: `ipsc-tracker`
   - **Database Password**: Create a strong password (SAVE THIS!)
   - **Region**: Choose closest to Germany (e.g., Frankfurt)
   - **Plan**: Free tier
6. Click **"Create new project"**
7. Wait 2-3 minutes for database to provision

### **STEP 2: Get Database Connection Details** (2 minutes)

1. In your Supabase project, click **"Settings"** (bottom left)
2. Click **"Database"**
3. Scroll to **"Connection string"**
4. Copy the **"URI"** (looks like: `postgresql://postgres:[YOUR-PASSWORD]@...`)
5. Save this somewhere safe - you'll need it!

Example:
```
postgresql://postgres.xxxxx:password@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
```

### **STEP 3: Run Migration Script** (5 minutes)

1. Open the file `migrate_to_supabase.py`
2. Update the connection details at the top:
   ```python
   SUPABASE_HOST = "aws-0-eu-central-1.pooler.supabase.com"  # From your URI
   SUPABASE_PASSWORD = "your-password-here"  # Your database password
   ```

3. Install PostgreSQL driver:
   ```powershell
   & "u:/DATA MANAGMENT/NT_Literature/iPSC_Tracker/.venv/Scripts/python.exe" -m pip install psycopg2-binary
   ```

4. Run the migration:
   ```powershell
   & "u:/DATA MANAGMENT/NT_Literature/iPSC_Tracker/.venv/Scripts/python.exe" migrate_to_supabase.py
   ```

5. Verify data in Supabase:
   - Go to Supabase dashboard
   - Click **"Table Editor"**
   - You should see: `cell_lines`, `passages`, `thaws`, `freezes`, etc.

### **STEP 4: Update App for PostgreSQL** (Already done! ✅)

The app will automatically detect if Supabase credentials are available and use PostgreSQL instead of SQLite.

### **STEP 5: Deploy to Streamlit Cloud** (5 minutes)

1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repository**: `Narasimhat/ipsc-tracker-daily-lab`
   - **Branch**: `master`
   - **Main file**: `app.py`
   - **App URL**: Choose a name (e.g., `ipsc-tracker-mdc`)

5. **BEFORE clicking Deploy**, click **"Advanced settings"**

6. Add **Secrets** (paste your Supabase connection string):
   ```toml
   [supabase]
   connection_string = "postgresql://postgres.xxxxx:password@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"
   ```

7. Click **"Save"** then **"Deploy!"**

8. Wait 2-3 minutes for deployment

### **STEP 6: Test Your App** (2 minutes)

1. Once deployed, you'll get a URL like:
   ```
   https://ipsc-tracker-mdc.streamlit.app
   ```

2. Open it and test:
   - ✅ Can you see existing cell lines?
   - ✅ Can you add a new entry?
   - ✅ Refresh the page - is data still there? (Should be!)
   - ✅ Check Supabase Table Editor - new data appears?

3. If everything works: **CONGRATULATIONS!** 🎉

---

## 📤 **Share with Your Team**

Send this message to your colleagues:

```
Hi team,

Our iPSC Tracker is now live in the cloud! 🎉

Access it here: https://ipsc-tracker-mdc.streamlit.app

Features:
✅ Works from anywhere (home, office, mobile)
✅ No installation needed
✅ Data persists automatically
✅ Real-time updates
✅ Automatic backups

Just bookmark the link and start using it!
```

---

## 🔒 **Security & Access**

### **Current Setup:**
- App is PUBLIC (anyone with URL can access)
- Database credentials are secure (stored in Streamlit secrets)

### **To Add Authentication:**
1. In Streamlit Cloud, go to your app settings
2. Enable "Password protection"
3. Or: Use Supabase Authentication (advanced - I can help later)

---

## 💰 **Costs**

### **Free Tier Includes:**
- **Supabase**: 
  - 500 MB database (plenty for years)
  - Automatic daily backups
  - Up to 2 GB bandwidth/month
  
- **Streamlit Cloud**:
  - 1 GB RAM
  - Unlimited apps
  - Auto-deploy from GitHub

### **If You Outgrow Free:**
- **Supabase Pro**: $25/month (unlikely you'll need this)
- **Streamlit Pro**: $20/month/user

---

## 🔄 **Updating Your App**

Just push to GitHub:
```powershell
git add .
git commit -m "Update app"
git push
```

Streamlit will automatically redeploy in 1-2 minutes!

---

## 📊 **Database Management**

### **View/Edit Data:**
- Supabase Dashboard → Table Editor
- You can manually edit, import, export

### **Backup Database:**
- Supabase → Database → Backups
- Download SQL dump anytime

### **Connect from Other Tools:**
- Use the connection string with:
  - DBeaver
  - pgAdmin
  - Python scripts
  - Excel (via ODBC)

---

## 🆘 **Troubleshooting**

### **App shows "Connection Error"**
- Check Streamlit secrets are set correctly
- Verify Supabase project is running
- Check connection string format

### **Data not appearing**
- Verify migration script ran successfully
- Check Supabase Table Editor
- Look at Streamlit logs

### **App is slow**
- Check Supabase dashboard for query performance
- Add indexes if needed (I can help)

### **Need help?**
- Supabase docs: https://supabase.com/docs
- Streamlit docs: https://docs.streamlit.io
- Ask me! I'm here to help 😊

---

## 🎯 **What You Get**

✅ **Professional cloud infrastructure**
✅ **Automatic backups** (daily)
✅ **Zero maintenance** (Supabase handles everything)
✅ **Scalable** (handles 100s of users)
✅ **Fast** (PostgreSQL is much faster than SQLite)
✅ **Secure** (encrypted connections, access control)
✅ **Real-time** (changes sync instantly)
✅ **FREE** (for your use case)

---

## 🌟 **Optional Enhancements** (Later)

I can add:
- User authentication (login system)
- Email notifications
- Advanced analytics
- Mobile app
- API access
- Automated reports

Just let me know! 🚀

---

**Ready to deploy? Let's do this!** 🎉

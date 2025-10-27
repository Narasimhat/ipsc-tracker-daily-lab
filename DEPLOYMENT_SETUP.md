# 🚀 iPSC Tracker - Streamlit Cloud Deployment Setup

## 🔐 **Authentication Configuration for Cloud Deployment**

### **Method 1: Simple Authentication (Recommended for Quick Start)**

Since we're using a simple form-based authentication system, the login credentials are defined in the code. For Streamlit Cloud deployment:

#### **Step 1: Deploy to Streamlit Cloud**
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - Repository: `Narasimhat/ipsc-tracker-daily-lab`
   - Branch: `master`
   - Main file: `app.py`
5. Click "Deploy!"

#### **Step 2: Default Login Credentials**
The app will deploy with these default credentials:
```
Admin User:
- Username: admin
- Password: admin123

Pro User:
- Username: scientist1  
- Password: password123

Member User:
- Username: member1
- Password: password123
```

### **Method 2: Secure Secrets Configuration (Production)**

For production use, configure secrets in Streamlit Cloud:

#### **Step 1: Access Secrets Management**
1. Go to your deployed app dashboard
2. Click "Settings" → "Secrets"
3. Add the following configuration:

```toml
# Copy this into Streamlit Cloud Secrets section:

[auth]
admin_user = "your_admin_username"
admin_password = "your_secure_password"
pro_user = "your_pro_username" 
pro_password = "your_pro_password"
member_user = "your_member_username"
member_password = "your_member_password"

[app]
environment = "production"
```

#### **Step 2: Update auth.py for Secrets**
The current simple authentication can be enhanced to read from Streamlit secrets in production.

---

## 🌐 **Quick Deployment Steps**

### **Immediate Deployment (5 minutes):**

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App:**
   - Repository: `Narasimhat/ipsc-tracker-daily-lab`
   - Branch: `master`
   - Main file: `app.py`
   - App URL: Choose a custom name (e.g., `ipsc-tracker-lab`)

3. **Click Deploy!**
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://your-app-name.streamlit.app`

4. **Login with default credentials:**
   ```
   Username: admin
   Password: admin123
   ```

5. **Share URL with team immediately!**

---

## 🔧 **Post-Deployment Configuration**

### **Option A: Keep Default Credentials (Simple)**
- Use the built-in credentials
- Good for demos and internal teams
- Share login info with authorized users

### **Option B: Customize Credentials (Secure)**
- Modify the authentication code
- Use Streamlit secrets for passwords
- Better for production environments

### **Option C: Add More Users**
- Edit the authentication logic
- Add more username/password combinations
- Implement team-based access

---

## 📊 **What Gets Deployed:**

✅ **Full iPSC Tracker with all features:**
- Professional authentication system
- Role-based access (Admin/Pro/Member)
- Advanced analytics and reporting
- Team collaboration features
- Data export capabilities
- Professional UI/UX

✅ **Default Access Levels:**
- **Admin:** Full system access, user management
- **Pro:** Advanced analytics, data export
- **Member:** Standard lab operations

✅ **No Configuration Needed:**
- Database auto-initializes
- All dependencies install automatically
- Authentication works immediately

---

## 🔒 **Security Considerations**

### **Default Setup:**
- App is publicly accessible via URL
- Authentication protects internal features
- URL should be shared only with authorized users

### **Enhanced Security Options:**
1. **Change default passwords immediately**
2. **Use Streamlit secrets for credentials**
3. **Implement IP whitelisting if needed**
4. **Set up regular data backups**

---

## 🎯 **Recommended Deployment Flow:**

1. **Deploy NOW with defaults** (5 minutes)
2. **Test all features work** (5 minutes)  
3. **Share with 1-2 trusted users** (immediate)
4. **Customize credentials later** (optional)
5. **Scale to full team** (when ready)

---

## 🚨 **Important Notes:**

- **Database resets** on app restart (Streamlit Cloud limitation)
- **Export data regularly** using built-in export features
- **Monitor app usage** via Streamlit Cloud dashboard
- **Free tier limits:** 1GB RAM, good for small teams

---

## ✅ **Ready to Deploy?**

Your iPSC Tracker is deployment-ready RIGHT NOW! 

Just go to https://share.streamlit.io and deploy with:
- Repo: `Narasimhat/ipsc-tracker-daily-lab`
- File: `app.py`
- Default login: `admin` / `admin123`

**Your team can start using it within 5 minutes!** 🎉
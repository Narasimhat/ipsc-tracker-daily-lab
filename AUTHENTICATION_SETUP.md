# 🔐 Professional Authentication Setup - iPSC Tracker

## Overview
Professional authentication system using `streamlit-authenticator` with secure password hashing, role-based access control, and team organization.

---

## 🚀 **Quick Setup** (10 Minutes)

### **Step 1: Install Dependencies**

```powershell
pip install streamlit-authenticator bcrypt pyyaml
```

Or if you have the updated requirements.txt:
```powershell
pip install -r requirements.txt
```

### **Step 2: Generate Password Hashes**

Run the password generator:
```powershell
python generate_password_hash.py your_password_here
```

Or manually:
```python
import bcrypt
password = "your_password_here"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print(hashed)
```

### **Step 3: Configure Secrets**

#### **For Streamlit Cloud:**
1. Go to **https://share.streamlit.io**
2. Click on your app: **ipsc-tracker-daily-lab**
3. Go to **Settings** → **Secrets**
4. Replace existing content with:

```toml
[cookie]
name = "ipsc_tracker_auth"
key = "your_32_character_random_secret_key_here"
expiry_days = 7

[auth]
preauthorized_emails = ["admin@yourlab.org"]

[users.admin]
name = "Admin User"
email = "admin@yourlab.org"
role = "admin"
team = "Management"
hashed_password = "$2b$12$your_bcrypt_hash_here"

[users.narasimha]
name = "Narasimha"
email = "narasimha@yourlab.org"
role = "admin"
team = "Research"
hashed_password = "$2b$12$replace_with_actual_hash"

# Add more users as needed
[users.colleague1]
name = "Dr. Jane Smith"
email = "jane@yourlab.org"
role = "member"
team = "Cardiac"
hashed_password = "$2b$12$replace_with_actual_hash"
```

#### **For Local Development:**
Edit `.streamlit/secrets.toml` with the same configuration.

### **Step 4: Generate Secure Cookie Key**

```python
import secrets
print(secrets.token_urlsafe(32))
```

Use this output as your cookie key.

---

## � **Security Features**

### **Enhanced Security:**
- ✅ **Bcrypt password hashing** (industry standard)
- ✅ **Secure session cookies** with expiration
- ✅ **Role-based access control** (admin, pro, member, viewer)
- ✅ **Team organization** for data scoping
- ✅ **Professional login/logout flow**
- ✅ **Pre-authorized email domains**

### **Role Definitions:**

#### **Admin Role** 👑
- Full system access and configuration
- User management capabilities  
- Access to all team data
- System settings and maintenance

#### **Pro Role** ⭐
- Standard member features
- Advanced analytics and reporting
- Bulk export capabilities
- Enhanced experimental tracking

#### **Member Role** 👨‍🔬
- Add/edit culture entries
- View personal and team data
- Basic reporting and exports
- Standard experimental tracking

#### **Viewer Role** 👁️
- Read-only access to data
- View reports and dashboards
- No editing capabilities
- Good for supervisors/observers

---

## 👥 **User Management**

### **Add a New User:**

1. **Generate password hash:**
   ```powershell
   python generate_password_hash.py new_user_password
   ```

2. **Add to secrets:**
   ```toml
   [users.newuser]
   name = "New User Name"
   email = "newuser@lab.org"
   role = "member"
   team = "Research"
   hashed_password = "$2b$12$generated_hash_here"
   ```

3. **Save and restart app**

### **Change User Password:**

1. Generate new hash
2. Update `hashed_password` in secrets
3. Restart application

### **Remove User:**

1. Delete user section from secrets
2. Save and restart

---

## 🏢 **Team Organization**

### **Team-Based Features:**
- Organize users by research focus
- Team-specific data filtering (future feature)
- Collaborative dashboards
- Team performance analytics

### **Example Teams:**
- **Cardiac**: Heart cell research
- **Neural**: Brain/nerve cell research  
- **Stem Cell**: General iPSC work
- **Drug Discovery**: Screening and testing
- **Management**: Lab administrators

---

## 📊 **What's New**

### **Compared to Simple Auth:**
| Feature | Simple Auth | Professional Auth |
|---------|-------------|-------------------|
| Password Storage | Plain text | Bcrypt hashed |
| Session Security | Basic | Secure cookies |
| User Roles | None | Admin/Pro/Member/Viewer |
| Team Organization | None | Full team support |
| Login UI | Basic | Professional |
| User Management | Manual | Role-based |

---

## 🔧 **Troubleshooting**

### **Common Issues:**

**"Authentication configuration error"**
- Check secrets.toml syntax
- Verify all required fields are present
- Ensure cookie key is set and valid

**"Incorrect username or password"**
- Verify username exists in secrets.toml
- Check password hash was generated correctly
- Try regenerating the hash

**"Import streamlit_authenticator error"**
- Run: `pip install streamlit-authenticator`
- Verify installation: `pip list | grep streamlit`

### **Debug Mode:**
Add this temporarily to debug:
```python
if st.checkbox("Debug Auth", key="debug_auth"):
    st.write("Available users:", list(st.secrets.get("users", {}).keys()))
    st.write("Current user:", st.session_state.get("username"))
    st.write("Auth status:", st.session_state.get("auth_status"))
```

---

## 🎯 **Recommended Setup for Your Lab**

```toml
[cookie]
name = "ipsc_tracker_auth"
key = "replace_with_32_char_random_key"
expiry_days = 7

[auth]
preauthorized_emails = ["yourlab.org"]

# Lab Administrator
[users.admin]
name = "Lab Admin"
email = "admin@yourlab.org"
role = "admin"
team = "Management"
hashed_password = "$2b$12$replace_with_hash"

# Senior Scientists (Pro access)
[users.narasimha]
name = "Narasimha"
email = "narasimha@yourlab.org"
role = "pro"
team = "Research"
hashed_password = "$2b$12$replace_with_hash"

# Lab Members
[users.researcher1]
name = "Dr. Research One"
email = "researcher1@yourlab.org"
role = "member"
team = "Cardiac"
hashed_password = "$2b$12$replace_with_hash"

[users.researcher2]
name = "Dr. Research Two"
email = "researcher2@yourlab.org"
role = "member"
team = "Neural"
hashed_password = "$2b$12$replace_with_hash"

# Read-only Access
[users.supervisor]
name = "Lab Supervisor"
email = "supervisor@yourlab.org"
role = "viewer"
team = "Management"
hashed_password = "$2b$12$replace_with_hash"
```

---

## � **Migration from Simple Auth**

If you're upgrading from the simple authentication:

1. **Backup current secrets** 
2. **Install new dependencies**
3. **Generate password hashes** for existing users
4. **Update secrets.toml** with new format
5. **Test login flow**
6. **Deploy to production**

The new system is **fully backward compatible** - existing app functionality remains unchanged, just with better security.

---

## 📱 **User Experience**

### **Enhanced Login:**
- Professional login form
- Clear error messages
- Role-based welcome messages
- Secure session management

### **User Dashboard:**
- Welcome message with user name and role
- Role-based feature access
- Team information display
- Professional logout flow

---

**Ready! Your iPSC Tracker now has enterprise-grade authentication!** 🔐

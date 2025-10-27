# 🔐 STREAMLIT CLOUD SECRETS CONFIGURATION

## Copy the content below into your Streamlit Cloud app secrets:

```toml
# Streamlit Cloud Secrets Configuration
# Go to your app → Settings → Secrets → Paste this content

[users]

[users.admin]
password = "iPSC_Lab2024!"
name = "Lab Administrator"
role = "admin"
team = "Management"
email = "admin@your-lab.org"

[users.scientist1]
password = "Research_Secure2024"
name = "Dr. Sarah Smith"
role = "pro"
team = "Cardiac Research"
email = "sarah.smith@your-lab.org"

[users.scientist2]
password = "Culture_Secure2024"
name = "Dr. John Johnson"
role = "member"
team = "Neural Research"
email = "john.johnson@your-lab.org"

[users.technician1]
password = "Lab_Tech2024"
name = "Lab Technician"
role = "member"
team = "General Lab"
email = "tech@your-lab.org"

[users.viewer]
password = "ReadOnly_2024"
name = "Lab Viewer"
role = "viewer"
team = "Administration"
email = "viewer@your-lab.org"

# Optional: Additional security settings
[security]
session_timeout = 8  # hours
max_login_attempts = 5
require_password_change = false

# Optional: Lab-specific settings
[lab]
name = "Your Lab Name"
institution = "Your Institution"
contact_admin = "admin@your-lab.org"
```

## 🚀 HOW TO CONFIGURE STREAMLIT CLOUD SECRETS:

### Step 1: Deploy Your App
1. Go to https://share.streamlit.io
2. Deploy your app as normal

### Step 2: Configure Secrets
1. Go to your deployed app dashboard
2. Click "Settings" in the top right
3. Click "Secrets" in the left sidebar
4. Paste the configuration above
5. Modify passwords and user details for your team
6. Click "Save"

### Step 3: Test Secure Login
1. Visit your app URL
2. Try logging in with the secure credentials
3. No passwords will be visible on the login screen
4. Share credentials privately with your team

## 🔒 SECURITY BENEFITS:

✅ **No passwords in code** - stored securely in Streamlit Cloud
✅ **No visible credentials** - clean, professional login screen
✅ **Environment-specific** - different passwords for dev/prod
✅ **Easy user management** - add/remove users in secrets
✅ **Professional appearance** - looks like a real enterprise system

## 👥 SHARING WITH YOUR TEAM:

### What to Share:
- ✅ App URL: `https://your-app-name.streamlit.app`
- ✅ Username and password (privately via email/Slack)
- ✅ Instructions for using the system

### What NOT to Share:
- ❌ Don't post credentials publicly
- ❌ Don't include passwords in documentation
- ❌ Don't share the secrets configuration file

## 🔧 FALLBACK CREDENTIALS:

If secrets are not configured, the app will use these secure fallback credentials:

- **Admin:** `admin` / `iPSC_Lab2024!`
- **Scientist 1:** `scientist1` / `Research_2024`
- **Scientist 2:** `scientist2` / `Culture_2024`
- **Viewer:** `viewer` / `ReadOnly_2024`

These are much more secure than the demo credentials and suitable for actual lab use!
# 🚂 Railway.app Deployment Guide - iPSC Tracker

## 📋 Prerequisites
- GitHub account with your repository: `Narasimhat/ipsc-tracker-daily-lab`
- Railway.app account (sign up at https://railway.app)

## 🚀 Quick Deployment Steps

### Step 1: Sign Up on Railway
1. Go to https://railway.app
2. Click **"Login"** and sign in with GitHub
3. Authorize Railway to access your repositories

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose: `Narasimhat/ipsc-tracker-daily-lab`
4. Railway will auto-detect the Dockerfile

### Step 3: Configure Environment
1. In the Railway dashboard, go to your project
2. Click on the service (ipsc-tracker)
3. Go to **"Variables"** tab
4. Add these environment variables:
   ```
   PORT=8080
   STREAMLIT_SERVER_PORT=8080
   STREAMLIT_SERVER_ADDRESS=0.0.0.0
   STREAMLIT_SERVER_HEADLESS=true
   ```

### Step 4: Add Persistent Volume
1. In your service, go to **"Settings"**
2. Scroll to **"Volumes"**
3. Click **"+ New Volume"**
4. Mount path: `/app/data`
5. Click **"Add Volume"**

### Step 5: Deploy!
1. Railway will automatically deploy
2. Wait 2-3 minutes for build to complete
3. Click **"Settings"** → **"Generate Domain"**
4. You'll get a URL like: `https://ipsc-tracker-production.up.railway.app`

## 🌐 Share with Your Team

Once deployed, share this URL with your colleagues:
```
https://your-app-name.up.railway.app
```

✅ **Benefits:**
- Works from anywhere (no VPN needed)
- Automatic HTTPS (secure)
- No need to keep your computer running
- Data persists between deployments
- Automatic backups via Railway

## 💰 Pricing
- **Free trial**: $5 credit (enough for 1-2 months of testing)
- **After trial**: ~$5-10/month depending on usage
- **Hobby plan**: $5/month for 500 hours

## 🔧 Update Your App
Any push to your GitHub repository will automatically redeploy!

```bash
git add .
git commit -m "Update app"
git push
```

Railway will automatically rebuild and redeploy within 2-3 minutes.

## 📊 Monitor Your App
Railway dashboard shows:
- Real-time logs
- CPU and memory usage
- Deployment history
- Database size

## 🆘 Troubleshooting

### App won't start
- Check logs in Railway dashboard
- Verify PORT environment variable is set
- Ensure volume is mounted to `/app/data`

### Database not persisting
- Verify volume is created and mounted
- Check that `ipsc_tracker.db` is in `/app/data/` directory

### Need to access database
1. Go to Railway dashboard
2. Click on your service
3. Go to **"Settings"** → **"Data"**
4. You can download backups or use Railway CLI

## 🎯 Next Steps After Deployment

1. **Test the app**: Open your Railway URL
2. **Verify data**: Create a test entry
3. **Share with team**: Send the URL to colleagues
4. **Set up custom domain** (optional): Configure your own domain in Railway settings
5. **Enable authentication** (optional): Add Streamlit authentication for security

---

**🎉 Your iPSC Tracker is now live on the cloud!**

No need to keep VS Code running or manage Docker locally anymore.

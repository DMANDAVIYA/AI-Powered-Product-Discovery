# Deployment Guide (FREE - No Payment Required!)

## 🎯 Overview

**What We're Deploying:**
- **Backend (FastAPI + PostgreSQL):** Render.com (Free)
- **Frontend (React + Vite):** Vercel.com (Free)
- **Database Migration:** Using backup files (saves Firecrawl credits!)

**Total Cost:** $0.00

---

## 📋 Prerequisites

✅ GitHub account
✅ Code pushed to GitHub
✅ Database backup created (`products_backup.json`)
✅ OpenAI API key
✅ Firecrawl API key (optional if using migration)

---

# PART 1: Deploy Backend to Render

## Step 1: Create Render Account

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with **GitHub** (recommended)
4. Verify your email

---

## Step 2: Create PostgreSQL Database

1. In Render dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Fill in:
   - **Name:** `neusearch-db`
   - **Database:** `neusearch`
   - **User:** `neusearch_user`
   - **Region:** Choose closest to you (e.g., Oregon)
   - **PostgreSQL Version:** 15
   - **Plan:** **Free** ⚠️ IMPORTANT!
4. Click **"Create Database"**
5. Wait 1-2 minutes for database to be created
6. **COPY THE CONNECTION STRING** (Internal Database URL):
   ```
   postgres://neusearch_user:xxxxx@dpg-xxxxx.oregon-postgres.render.com/neusearch
   ```
   postgresql://neusearch_user:xBzGEv12v5BNaBbZvofpVqhnWkLu5aM5@dpg-d4qk1vuuk2gs73fo9feg-a/neusearch
   Save this - you'll need it!

---

## Step 3: Deploy Backend Web Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Click **"Connect account"** → Select **GitHub**
3. Find and select your repository: `AI-Powered-Product-Discovery`
4. Click **"Connect"**

### Configure Web Service:

**Basic Settings:**
- **Name:** `neusearch-backend`
- **Region:** Same as database (e.g., Oregon)
- **Branch:** `main`
- **Root Directory:** (leave empty)

**Build Settings:**
- **Runtime:** `Docker`
- **Dockerfile Path:** `Dockerfile`

**OR if not using Docker:**
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- **Plan:** **Free** ⚠️ IMPORTANT!

---

## Step 4: Add Environment Variables

Scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** and add these:

```
DATABASE_URL = [paste your PostgreSQL connection string from Step 2]
OPENAI_API_KEY = [your OpenAI API key]
FIRECRAWL_API_KEY = [your Firecrawl API key]
```

**Example:**
```
DATABASE_URL = postgres://neusearch_user:abc123@dpg-xyz.oregon-postgres.render.com/neusearch
OPENAI_API_KEY = sk-proj-xxxxxxxxxxxxx
FIRECRAWL_API_KEY = fc-xxxxxxxxxxxxx
```

---

## Step 5: Deploy!

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Watch the logs - should see "Build successful"
4. Your backend URL will be: `https://neusearch-backend.onrender.com`

**Test it:**
Visit: `https://neusearch-backend.onrender.com`
Should see: `{"message": "Neusearch AI Backend is running"}`

---

## Step 6: Populate Database (Migration Method)

**Option A: Import from Backup (Recommended - Saves Credits!)**

1. Go to your backend URL: `https://neusearch-backend.onrender.com/docs`
2. You'll see FastAPI Swagger docs
3. Find `/import-backup` endpoint
4. Click "Try it out" → "Execute"
5. Wait 30 seconds
6. Done! Database populated with 25 products

**OR use Render Shell:**
1. Go to Render dashboard → Your web service
2. Click **"Shell"** tab
3. Run: `python -m backend.import_db`

**Option B: Re-scrape (Uses Firecrawl Credits)**

Visit: `https://neusearch-backend.onrender.com/scrape`
Wait 2-3 minutes

---

## Step 7: Verify Backend

Test these endpoints:

```bash
# Check backend is running
https://neusearch-backend.onrender.com/

# Check products
https://neusearch-backend.onrender.com/products

# Test chat
https://neusearch-backend.onrender.com/docs
```

✅ **Backend deployed successfully!**

**Save your backend URL:** `https://neusearch-backend.onrender.com`

---

# PART 2: Deploy Frontend to Vercel

## Step 1: Update API URLs in Frontend

Before deploying, update the API URL in your frontend code.

**Update these 3 files:**

1. `frontend/src/pages/Home.jsx` - Line 7
2. `frontend/src/pages/ProductDetail.jsx` - Line 7  
3. `frontend/src/components/ChatInterface.jsx` - Line 7

Change from:
```javascript
const API_URL = 'http://127.0.0.1:8000'
```

To:
```javascript
const API_URL = 'https://neusearch-backend.onrender.com'
```

**OR use the PowerShell script:**
```powershell
.\update-api-url.ps1 -BackendUrl "https://neusearch-backend.onrender.com"
```

**Commit and push:**
```bash
git add .
git commit -m "Update API URL for production"
git push origin main
```

---

## Step 2: Create Vercel Account

1. Go to https://vercel.com
2. Click **"Sign Up"**
3. Sign up with **GitHub** (recommended)
4. Authorize Vercel to access your GitHub

---

## Step 3: Deploy Frontend

1. In Vercel dashboard, click **"Add New..."** → **"Project"**
2. Click **"Import Git Repository"**
3. Find your repo: `AI-Powered-Product-Discovery`
4. Click **"Import"**

### ⚠️ CRITICAL: Configure Build Settings

**Before clicking Deploy, configure these:**

**Framework Preset:**
- Select: **Vite**

**Root Directory:** ⚠️ MOST IMPORTANT!
- Click **"Edit"** next to Root Directory
- Type: `frontend`
- Click **"Continue"**

**Build Settings** (auto-filled):
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

**Environment Variables:**
- Leave empty (frontend doesn't need any)

---

## Step 4: Deploy!

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. You'll see "Congratulations!" when done
4. Your frontend URL: `https://ai-powered-product-discovery-xxx.vercel.app`

---

## Step 5: Test Deployment

Visit your Vercel URL and test:

✅ Products load on home page
✅ Click a product → detail page works
✅ Click "CHAT" → chat interface opens
✅ Search for "crewneck" → AI responds with products
✅ "View on Website" button works

---

# 🎉 Deployment Complete!

## Your Live URLs:

- **Frontend:** `https://ai-powered-product-discovery-xxx.vercel.app`
- **Backend:** `https://neusearch-backend.onrender.com`
- **Database:** Render PostgreSQL (internal)

---

## 📊 Free Tier Limitations

### Render Free Tier:
- ✅ 750 hours/month (24/7 uptime)
- ⚠️ Sleeps after 15 mins of inactivity
- ⚠️ First request after sleep: ~30 seconds to wake up
- ✅ 512 MB RAM
- ✅ Shared CPU

### Vercel Free Tier:
- ✅ Unlimited deployments
- ✅ 100 GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Instant global CDN

**Note:** First request to backend after 15 mins will be slow (cold start). This is normal for free tier!

---

## 🔧 Troubleshooting

### Backend Issues:

**Build fails:**
- Check `requirements.txt` has all dependencies
- Check Dockerfile syntax
- View build logs in Render dashboard

**Database connection error:**
- Verify `DATABASE_URL` is correct
- Check PostgreSQL database is running
- Try internal vs external connection string

**API endpoints return 500:**
- Check environment variables are set
- View logs in Render dashboard
- Ensure OpenAI API key is valid

### Frontend Issues:

**Blank page:**
- Check browser console for errors
- Verify API URL is correct
- Check CORS settings in backend

**Products don't load:**
- Verify backend is running
- Check API URL in frontend code
- Test backend endpoints directly

**CORS errors:**
- Backend should allow Vercel domains
- Check `backend/main.py` CORS settings

### Vercel "No fastapi entrypoint" Error:

This means Vercel is looking in the wrong directory!

**Fix:**
1. Go to Vercel project settings
2. Find "Root Directory"
3. Set to: `frontend`
4. Redeploy

---

## 🚀 Next Steps

1. ✅ Test all features thoroughly
2. ✅ Record Loom video demo (2-3 mins)
3. ✅ Update README with deployment URLs
4. ✅ Submit assignment via Google Form

---

## 📝 Deployment Checklist

- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Backend deployed to Render
- [ ] Environment variables set
- [ ] Database populated (migration or scrape)
- [ ] Backend endpoints tested
- [ ] Frontend API URLs updated
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] Root directory set to `frontend`
- [ ] All features tested on live site
- [ ] Deployment URLs saved

---

## 💡 Tips

- **Cold starts:** First request after 15 mins will be slow (Render free tier)
- **Debugging:** Use Render logs and browser console
- **Updates:** Push to GitHub → Auto-deploys to Vercel
- **Backend updates:** Push to GitHub → Auto-deploys to Render

---

## 📚 Resources

- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI on Render](https://render.com/docs/deploy-fastapi)
- [Vite on Vercel](https://vercel.com/docs/frameworks/vite)

---

**Need help?** Check the logs in Render/Vercel dashboards!

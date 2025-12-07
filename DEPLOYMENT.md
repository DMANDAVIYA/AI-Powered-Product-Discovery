# Deployment Guide (FREE - No Payment Required!)

## Overview
We'll deploy:
- **Backend + PostgreSQL:** Render (Free tier)
- **Frontend:** Vercel (Free tier)
- **ChromaDB:** Persisted to disk on Render

---

## PART 1: Deploy Backend to Render

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email
4. Verify your email

### Step 2: Create PostgreSQL Database
1. In Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Fill in:
   - **Name:** `neusearch-db`
   - **Database:** `neusearch`
   - **User:** `neusearch_user`
   - **Region:** Choose closest to you
   - **Plan:** **Free** (Important!)
4. Click "Create Database"
5. **SAVE THE CONNECTION STRING** - you'll see it like:
   ```
   postgres://neusearch_user:xxxxx@dpg-xxxxx.oregon-postgres.render.com/neusearch
   ```

### Step 3: Push Code to GitHub
1. Open terminal in project folder
2. Run these commands:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
3. Create new repo on GitHub (https://github.com/new)
   - Name: `neusearch-ai`
   - Public repository
   - Don't initialize with README
4. Push code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/neusearch-ai.git
   git branch -M main
   git push -u origin main
   ```

### Step 4: Deploy Backend on Render
1. In Render dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `neusearch-ai` repo
4. Fill in:
   - **Name:** `neusearch-backend`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** `Python 3`
   - **Build Command:** `bash build.sh`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** **Free** (Important!)

5. **Add Environment Variables** (click "Advanced" → "Add Environment Variable"):
   ```
   DATABASE_URL = [paste your PostgreSQL connection string from Step 2]
   OPENAI_API_KEY = [your OpenAI API key]
   FIRECRAWL_API_KEY = [your Firecrawl API key]
   ```

6. Click "Create Web Service"
7. Wait 5-10 minutes for deployment
8. **SAVE YOUR BACKEND URL** - will be like: `https://neusearch-backend.onrender.com`

### Step 5: Initialize Database
1. Once deployed, go to your backend URL: `https://neusearch-backend.onrender.com`
2. You should see: `{"message": "Neusearch AI Backend is running"}`
3. Run scraper to populate database:
   - Use Postman or curl:
   ```bash
   curl -X POST https://neusearch-backend.onrender.com/scrape
   ```
   - Or visit in browser: `https://neusearch-backend.onrender.com/scrape`

---

## PART 2: Deploy Frontend to Vercel

### Step 1: Update Frontend API URL
1. Open `frontend/src/pages/Home.jsx`
2. Change line 7 from:
   ```javascript
   const API_URL = 'http://127.0.0.1:8000'
   ```
   To:
   ```javascript
   const API_URL = 'https://neusearch-backend.onrender.com'
   ```

3. Do the same in:
   - `frontend/src/pages/ProductDetail.jsx`
   - `frontend/src/components/ChatInterface.jsx`

4. Commit changes:
   ```bash
   git add .
   git commit -m "Update API URL for production"
   git push
   ```

### Step 2: Create Vercel Account
1. Go to https://vercel.com
2. Click "Sign Up"
3. Sign up with GitHub (recommended)

### Step 3: Deploy Frontend
1. In Vercel dashboard, click "Add New..." → "Project"
2. Import your `neusearch-ai` repository
3. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Click "Deploy"
5. Wait 2-3 minutes
6. **SAVE YOUR FRONTEND URL** - will be like: `https://neusearch-ai.vercel.app`

---

## PART 3: Test Deployment

1. Visit your frontend URL: `https://neusearch-ai.vercel.app`
2. Check:
   - ✅ Products load on home page
   - ✅ Click on a product → detail page works
   - ✅ Chat button works
   - ✅ Search for "crewneck" → AI responds

---

## Troubleshooting

### Backend Issues:
- **Build fails:** Check `requirements.txt` has all dependencies
- **Database error:** Verify DATABASE_URL is correct
- **API keys:** Make sure environment variables are set

### Frontend Issues:
- **Blank page:** Check browser console for errors
- **API errors:** Verify backend URL is correct
- **CORS errors:** Backend should allow Vercel domains

### ChromaDB:
- **Vector search fails:** ChromaDB will recreate on first use
- **Data persistence:** Render Free tier has limited disk space

---

## Free Tier Limitations

**Render Free:**
- ✅ 750 hours/month (enough for 24/7)
- ⚠️ Sleeps after 15 mins of inactivity (wakes up in ~30 seconds)
- ✅ 512 MB RAM
- ✅ Shared CPU

**Vercel Free:**
- ✅ Unlimited deployments
- ✅ 100 GB bandwidth/month
- ✅ Automatic HTTPS

**Note:** First request after sleep will be slow (~30 seconds). This is normal for free tier!

---

## Next Steps After Deployment

1. ✅ Test all features
2. ✅ Record Loom video demo
3. ✅ Update README with deployment URLs
4. ✅ Submit assignment

---

## Need Help?

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Check deployment logs in dashboard for errors

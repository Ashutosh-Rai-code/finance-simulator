# 🚀 Deployment Guide - Step by Step

Complete instructions to deploy your AI Financial Coach on the internet for free/low-cost and keep it live even when your laptop is off.

---

## 📋 Requirements Before Deployment

1. **GitHub account** (for storing code)
2. **Google Gemini API key** (for AI features)
3. **Cloud hosting account** (we'll use free tier options)
4. **Custom domain** (optional, but recommended)

---

## Option 1: Vercel (Frontend) + Render (Backend) - **RECOMMENDED FOR BEGINNERS**

### Why this combination?
- **Vercel**: Auto-deploys React frontend from GitHub, completely free
- **Render**: Free tier for backend with persistent storage
- **Total cost**: FREE (with some limitations)

---

### Step 1: Push code to GitHub

```bash
# Initialize git repo (if not already done)
cd c:\python_work\finance_simulator
git init
git add .
git commit -m "Initial commit"

# Create repo on github.com and add remote
git remote add origin https://github.com/YOUR_USERNAME/finance-simulator.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy Backend to Render

1. **Create Render account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub (easy!)

2. **Create new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select `finance-simulator` repo
   - Set the service's Root Directory to `backend` if Render supports monorepo roots.
   - Set Build Command: `pip install -r requirements.txt`
   - Set Start Command: `python -m uvicorn main:app --host 0.0.0.0 --port 8000`
   - Add Environment Variables:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     AI_API_ENABLED=true
     FRONTEND_URL=https://your-frontend-url.vercel.app
     ```
   - Deploy

   > If Render fails with a `Preparing metadata (pyproject.toml)` error, switch this service to Docker deployment instead of the Python buildpack or ensure Render is targeting the `backend` folder. The repo now includes `backend/pyproject.toml` for Python package metadata.
   > For Docker on Render, set `Dockerfile location` to `backend/Dockerfile` and leave Build Command blank.

3. **Get your backend URL**
   - After deployment, you'll get: `https://your-backend-name.onrender.com`
   - Save this URL

---

### Step 3: Deploy Frontend to Vercel

1. **Create Vercel account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import your project**
   - Click "Add New" → "Project"
   - Select your GitHub repo
   - Set Root Directory: `frontend`
   - Add Environment Variable:
     ```
     VITE_API_URL=https://your-backend-name.onrender.com/api
     ```
   - Deploy

3. **You're live!**
   - Visit your frontend URL
   - Visitor counter will track unique visitors
   - AI features work automatically

---

### Cost Summary
| Service | Free Tier | Cost |
|---------|-----------|------|
| Render Backend | 750 free hours/month (enough for continuous deployment) | FREE* |
| Vercel Frontend | Up to 100GB bandwidth | FREE |
| Domain (optional) | - | $10-15/year |
| **Total** | **Both free for typical use** | **FREE** |

*Render free tier spins down after 15 mins inactivity, but restarts automatically on request.

---

## Option 2: Heroku (Backend) + Netlify (Frontend)

### Step 1: Deploy Backend to Heroku

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
   ```bash
   heroku login
   cd c:\python_work\finance_simulator
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set GEMINI_API_KEY=your_gemini_api_key_here
   heroku config:set AI_API_ENABLED=true
   heroku config:set FRONTEND_URL=https://your-frontend.netlify.app
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Get your backend URL**
   - It will be: `https://your-app-name.herokuapp.com`

---

### Step 2: Deploy Frontend to Netlify

1. **Create Netlify account**
   - Go to [netlify.com](https://netlify.com)
   - Sign up with GitHub

2. **Connect your repo**
   - Click "Add new site" → "Import an existing project"
   - Select GitHub repo
   - Set Build command: `cd frontend && npm run build`
   - Set Publish directory: `frontend/dist`
   - Add Build Env Variable:
     ```
     VITE_API_URL=https://your-app-name.herokuapp.com/api
     ```
   - Deploy

3. **Site is live!**

---

## Option 3: Railway (Backend) + Vercel (Frontend) - EASIEST

### Step 1: Deploy Backend to Railway

1. **Create Railway account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repo
   - Set service root: `backend`
   - Add variables:
     ```
     GEMINI_API_KEY=your_key
     AI_API_ENABLED=true
     FRONTEND_URL=https://your-frontend.vercel.app
     ```

3. **Deploy automatically**
   - Railway auto-deploys when you push to GitHub

---

### Step 2: Deploy Frontend to Vercel (same as Option 1, Step 3)

---

## Option 4: Google Cloud Run (Backend) + Vercel (Frontend)

### Step 1: Deploy Backend to Google Cloud Run

1. **Create Google Cloud account**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Create a new project

2. **Enable Cloud Run API**
   - Search "Cloud Run" → Enable it
   - Search "Artifact Registry" → Enable it

3. **Deploy from GitHub**
   - Cloud Run → Create Service
   - Select "Continuously deploy from a Git repository"
   - Connect GitHub repo
   - Set `Dockerfile location`: `backend/Dockerfile` (you need to create this)
   - Deploy

4. **Get your service URL**
   - Something like: `https://your-service-xxxxx.run.app`

---

## Option 5: AWS (Backend) + Vercel (Frontend)

### Step 1: Deploy Backend to AWS Elastic Beanstalk

1. **Create AWS account**
   - Go to [aws.amazon.com](https://aws.amazon.com)
   - Enable free tier

2. **Install AWS CLI**
   ```bash
   pip install awsebcli
   ```

3. **Initialize Elastic Beanstalk**
   ```bash
   cd backend
   eb init -p python-3.11 your-app-name
   eb create your-app-env
   eb setenv GEMINI_API_KEY=your_key AI_API_ENABLED=true
   eb deploy
   ```

4. **Get your backend URL**
   - Check AWS console or use: `eb open`

---

## 🎯 RECOMMENDED: Vercel + Render Setup (Complete Walkthrough)

### Prerequisites:
- ✅ Code pushed to GitHub
- ✅ Render & Vercel accounts created
- ✅ Gemini API key ready

### Complete Steps:

**1. Update your code for production**
```bash
# backend/.env should have:
GEMINI_API_KEY=your_key_here
AI_API_ENABLED=true
```

**2. Create backend/requirements.txt** (if missing)
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
google-generativeai==0.3.0
```

**3. Push to GitHub**
```bash
git add -A
git commit -m "Production ready"
git push origin main
```

**4. Deploy Backend (Render)**
- Visit render.com
- New Web Service
- Connect GitHub repo
- Runtime: Python
- Build: `pip install -r backend/requirements.txt`
- Start: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000`
- Environment Variables:
  ```
  GEMINI_API_KEY=your_gemini_key
  AI_API_ENABLED=true
  FRONTEND_URL=https://your-vercel-url.vercel.app
  ```
- Deploy & wait 5-10 minutes

**5. Deploy Frontend (Vercel)**
- Visit vercel.com
- Import Project
- Select your repo
- Root Directory: `frontend`
- Environment: `VITE_API_URL=https://your-render-service.onrender.com/api`
- Deploy

**6. Test**
- Visit your Vercel frontend URL
- Try budget calculations
- Check unique visitor count in Insights

---

## 🔒 Security Best Practices

### For production:
1. **Never commit `.env` files**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Set API keys in deployment platform, not code**
   - Render: Environment Variables section
   - Vercel: Settings → Environment Variables

3. **Enable CORS restrictions**
   - Update `backend/main.py` origins to only allow your frontend domain

4. **Use HTTPS everywhere**
   - All cloud platforms provide free SSL

---

## 📊 Monitoring & Logs

### Check backend logs:
- **Render**: Dashboard → Logs
- **Vercel**: Deployments → Logs
- **Heroku**: `heroku logs --tail`

### Check visitor count:
```bash
# Via API
curl https://your-backend.onrender.com/api/visitors
```

---

## 🆘 Troubleshooting

### "Frontend can't connect to backend"
- Check `VITE_API_URL` in Vercel settings
- Confirm backend URL is correct
- Check CORS in `backend/main.py`

### "Gemini API not working"
- Verify `GEMINI_API_KEY` is set
- Check quota at console.cloud.google.com
- Wait a few minutes if you just set it

### "Visitor counter not showing"
- Check `/api/visitors` endpoint works: `curl your-backend/api/visitors`
- Clear browser cache
- Check browser console for errors

### "My backend goes to sleep"
- **Render free tier**: Spins down after 15 mins → restarts on request (5-10 sec delay)
- **Solution**: Upgrade to paid ($15/month) or use Railway/Heroku

---

## ✅ Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed & URL saved
- [ ] Frontend deployed & URL saved
- [ ] `VITE_API_URL` updated in frontend
- [ ] `FRONTEND_URL` updated in backend
- [ ] Gemini API key configured
- [ ] `AI_API_ENABLED=true` in backend
- [ ] Visited frontend URL - works?
- [ ] Click "Get Advice" - AI response?
- [ ] Check Insights page - visitor count shows?
- [ ] Share your public URL!

---

## 📱 Custom Domain (Optional)

### Add custom domain to Vercel
1. Go to Vercel Project Settings
2. Domains → Add custom domain
3. Update DNS records at your domain registrar
4. Wait 1-2 hours for propagation

### Add custom domain to Render (Backend)
1. Render Dashboard → Service Settings
2. Custom Domains → Add
3. Update DNS at your registrar

---

## 🎉 You're Live!

Your app is now:
✅ **Running on the internet** - accessible 24/7
✅ **Works when laptop is off** - hosted on cloud servers
✅ **Free tier** - Vercel + Render completely free
✅ **Auto-deploys** - push to GitHub, auto-redeploy
✅ **Tracks visitors** - unique visitor count in Insights

**Share your URL with friends and family! 🚀**

---

## Next Steps

1. **Add custom domain** (looks professional)
2. **Enable Google Analytics** (track traffic)
3. **Add password protection** (optional, for privacy)
4. **Set up monitoring** (alerts if backend is down)
5. **Upgrade to paid tiers** if you need:
   - Unlimited bandwidth
   - Always-on backend (no sleep)
   - Custom infrastructure

---

**Questions? Check logs, read cloud provider docs, or debug locally first!**

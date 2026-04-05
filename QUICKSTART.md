# Quick Start Guide - 5 Minutes to Running

## Prerequisites
- Python 3.9+
- Node.js 16+
- Docker (optional, but recommended)

---

## 🚀 Fastest Way (Using Docker)

```bash
# 1. Get Gemini API Key from: https://makersuite.google.com/app/apikey

# 2. In backend/.env, add:
GEMINI_API_KEY=your_key_here

# 3. Run everything:
docker-compose up

# 4. Open browser:
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

**That's it! ✅ App is running**

---

## Manual Setup (Without Docker)

### Step 1: Backend (Terminal 1)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GEMINI_API_KEY=your_key_here > .env

# Run server
python -m uvicorn main:app --reload
```

✅ Backend running at: http://localhost:8000

### Step 2: Frontend (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo VITE_API_URL=http://localhost:8000/api > .env.local

# Start dev server
npm run dev
```

✅ Frontend running at: http://localhost:3000

---

## What You'll See

### Dashboard Tab
- 📊 Financial metrics (Income, Expenses, Savings, SIP)
- 📈 Savings rate, emergency fund status
- 🎯 Goal progress bar
- ⚠️ Risk analysis
- 💬 AI financial coach with personalized advice
- 🔮 What-if simulator

### Quit Job Tab
- 💼 Job exit readiness analysis
- 📅 How many months can you survive
- 📊 Risk assessment
- 💡 Recommendations

---

## Test It Out

### Try These Actions

1. **Adjust Income Slider** → See metrics update in real-time
2. **Click "Get Advice"** → AI generates personalized 30/90/1-year plans
3. **Toggle Theme** → Switch between dark/light mode
4. **What-If Simulator** → See wealth impact of SIP changes
5. **Quit Job Tab** → Check if you're ready to leave job

---

## Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_gemini_api_key
AI_API_ENABLED=false
FRONTEND_URL=http://localhost:3000
```

- `AI_API_ENABLED=false` prevents Gemini API calls during normal development or testing.
- AI features only execute Gemini calls when the UI explicitly requests them.

Get API key: https://makersuite.google.com/app/apikey

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000/api
```

---

## Important Ports

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend App**: http://localhost:3000

If ports are in use, modify:
- Backend: Edit `docker-compose.yml` or add `--port 8001` to uvicorn
- Frontend: Edit `vite.config.ts` server.port

---

## Troubleshooting

### Backend Won't Start
```bash
# Check if Python is installed
python --version

# Check if port 8000 is free
lsof -i :8000

# Clear pip cache and reinstall
pip cache purge
pip install -r requirements.txt
```

### Frontend Won't Start
```bash
# Check if Node is installed
node --version

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 is free
lsof -i :3000
```

### API Not Connecting
1. Make sure backend is running: `http://localhost:8000/health`
2. Check `VITE_API_URL` in frontend `.env.local`
3. Check browser console for CORS errors
4. Restart both servers

### AI Features Not Working
1. Verify `GEMINI_API_KEY` is set in backend `.env`
2. Test API key validity
3. Check API usage limits in Google Cloud Console

---

## Next Steps

1. ✅ Get it running (follow above)
2. � **Test mobile responsiveness** (see below)
3. 📖 Read `README.md` for full documentation
4. 🛠️ Read `DEVELOPMENT.md` for development setup
5. 🏗️ Read `PROJECT_STRUCTURE.md` for architecture details
6. 📱 Read `MOBILE_RESPONSIVENESS.md` for mobile device details
7. 🚀 **Read `DEPLOYMENT.md` for internet deployment** ← Deploy your app live!
8. 🌍 Deploy using Vercel (frontend) + Render (backend) - completely FREE!

---

## 📱 Test Mobile Responsiveness

Before deploying, verify mobile compatibility:

### Quick Desktop Test (No Phone Needed)
1. **Open app**: http://localhost:3000
2. **Press F12** (Developer Tools)
3. **Click device icon** (top-left of DevTools)
4. **Select device**: iPhone 13, iPad, or Galaxy S21
5. **Rotate device** to test landscape mode
6. **Try interactions**: 
   - Adjust sliders
   - Click buttons
   - Toggle sidebar
   - Navigate pages

### Signs of Good Mobile Responsiveness ✅
- [ ] No horizontal scrolling (except data tables)
- [ ] All buttons are easy to tap (large enough)
- [ ] Text is readable without zooming
- [ ] Sidebar collapses on mobile
- [ ] Forms stack vertically
- [ ] Spacing looks balanced

### On Real Device (Optional)
1. Get your app URL from deployment
2. Visit URL on your phone/tablet
3. Test all features
4. Share feedback!

---

## Production Deployment

### Option A: Docker Hub
```bash
docker build -t yourname/ai-financial-coach-backend backend/
docker build -t yourname/ai-financial-coach-frontend frontend/
docker push yourname/ai-financial-coach-backend
docker push yourname/ai-financial-coach-frontend
```

### Option B: Cloud Platforms

**Heroku**
```bash
git push heroku main
```

**AWS ECS/Fargate**
- Push images to ECR
- Create task definitions
- Run tasks

**Google Cloud Run**
- Push images to Container Registry
- Deploy containers

**Azure App Service**
- Deploy Docker containers
- Configure environment variables

---

## Key Features

✅ Financial metrics calculation
✅ Risk analysis with recommendations  
✅ 10-year wealth roadmap visualization
✅ What-if scenarios simulator
✅ AI-powered personalized advice
✅ Quit job readiness analysis
✅ Dark/Light theme
✅ **Fully responsive (mobile/tablet/desktop)**
✅ Modern UI with real-time updates
✅ Production-ready API

---

## Architecture Overview

```
┌─────────────────────────────────┐
│    Browser (React)              │
│  localhost:3000                 │
└────────────┬────────────────────┘
             │ HTTP/REST
             ↓
┌─────────────────────────────────┐
│    FastAPI Server               │
│  localhost:8000                 │
│  - Financial Calculations       │
│  - AI Integration               │
│  - Data Validation              │
└─────────────────────────────────┘
```

---

## Common Commands

```bash
# Backend
python -m uvicorn main:app --reload
python -m uvicorn main:app --port 8001

# Frontend
npm run dev
npm run build
npm run preview

# Docker
docker-compose up
docker-compose up -d
docker-compose down

# Testing API
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

---

## Need Help?

1. Check browser console: F12 → Console tab
2. Check backend logs: Look at terminal where uvicorn is running
3. Read documentation: README.md, DEVELOPMENT.md, PROJECT_STRUCTURE.md
4. Check API docs: http://localhost:8000/docs

---

## Files to Customize

- `frontend/src/App.tsx` - Main app component
- `frontend/vite.config.ts` - Build configuration
- `backend/main.py` - API configuration
- `backend/services.py` - Business logic
- CSS files - Styling & themes

---

**🎉 You're ready to go! Start with: `docker-compose up`**

Happy building! 🚀

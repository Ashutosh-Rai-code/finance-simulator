# AI Financial Coach - Full Stack Application

A modern, AI-powered financial planning application with a React frontend and FastAPI backend. Get personalized financial advice, track progress towards goals, and simulate financial scenarios.

## 🏗️ Architecture

```
AI Financial Coach
├── Backend (FastAPI)
│   ├── Financial Calculations
│   ├── AI Coach Integration (Gemini)
│   ├── REST API
│   └── CORS Support
│
└── Frontend (React + TypeScript)
    ├── Modern UI Components
    ├── Real-time Data Visualization
    ├── Responsive Design
    └── Interactive Simulators
```

## ✨ Features

### Dashboard
- **Financial Metrics** - Real-time calculation of savings rate, emergency fund, SIP ratio
- **Goal Progress** - Visual tracking towards your financial target
- **Risk Analysis** - Identify financial risks and get recommendations
- **Wealth Roadmap** - 10-year projection with data visualization
- **What-If Simulator** - Experiment with different SIP amounts
- **AI Coach** - Personalized 30-day, 90-day, and 1-year financial plans

### Quit Job Analysis
- Determine if you're financially ready to leave your job
- Calculate survival months with current savings
- Get personalized risk assessment and recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Google Gemini API Key (optional, for AI features)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env .env.local
# Edit .env.local and add your GEMINI_API_KEY

# Run the server
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env.local

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

## 📚 API Documentation

### Financial Endpoints

#### Calculate Metrics
```
POST /api/financial/metrics
Body: {
  income: number,
  expenses: number,
  savings: number,
  sip: number,
  target_goal: number
}
```

#### Analyze Risks
```
POST /api/financial/risks
Body: { same as above }
```

#### Get Roadmap
```
POST /api/financial/roadmap
Body: { same as above }
```

#### What-If Simulation
```
POST /api/financial/what-if
Body: { 
  ...financial_data,
  new_sip: number 
}
```

### AI Endpoints

#### Get Personalized Advice
```
POST /api/ai/advice
Body: { financial_data }
```

#### Quit Job Analysis
```
POST /api/ai/quit-job-analysis
Body: { 
  savings: number, 
  expenses: number 
}
```

## 🎨 UI Components

### Core Components
- **MetricsCard** - Display financial metrics with trends
- **ProgressBar** - Visual goal progress indicator
- **RiskCard** - Risk analysis with recommendations
- **InputPanel** - Financial input sliders
- **RoadmapChart** - Wealth projection visualization
- **WhatIfSimulator** - Interactive scenario testing
- **AICoachPanel** - AI-generated advice display

### Pages
- **Dashboard** - Main financial overview
- **QuitJobPage** - Job exit readiness analysis

## 🛠️ Development

### Backend Structure
```
backend/
├── main.py              # FastAPI app
├── models.py            # Pydantic models
├── services.py          # Business logic
├── routes/
│   ├── financial.py     # Financial endpoints
│   └── ai_coach.py      # AI endpoints
└── requirements.txt
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/          # Page-level components
│   ├── services/       # API integration
│   ├── styles/         # Global styles
│   ├── App.tsx         # Root component
│   └── main.tsx        # Entry point
├── index.html
└── vite.config.ts
```

## 🔐 Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_api_key_here
AI_API_ENABLED=false
FRONTEND_URL=http://localhost:3000
```

- `AI_API_ENABLED=false` helps avoid Gemini API calls during development and testing.
- Enable this in production only when you want live AI responses from the UI.

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
```

## 📦 Production Build

### Backend
```bash
cd backend
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend
```bash
cd frontend
npm run build
# dist/ folder ready for deployment
```

---

## 🌍 Deploy on the Internet

**Read [DEPLOYMENT.md](DEPLOYMENT.md) for complete step-by-step instructions to deploy:**
- ✅ Vercel (Frontend) + Render (Backend) - **FREE**
- ✅ Heroku + Netlify - Free tier available
- ✅ Railway - Simple GitHub integration
- ✅ AWS, Google Cloud, Azure - Enterprise options
- ✅ Includes security best practices and troubleshooting

**Recommended for beginners**: Vercel + Render (5 minutes to deploy!)

---

## 🐳 Docker Deployment

### Docker Compose (Optional)
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

## 📱 Responsive Design

- **Desktop** - Full feature set with side navigation
- **Tablet** - Optimized grid layout
- **Mobile** - Touch-friendly interface with collapsible navigation

**For detailed mobile testing info, see [MOBILE_RESPONSIVENESS.md](MOBILE_RESPONSIVENESS.md)**

## 🎯 Key Technologies

### Backend
- FastAPI - Modern Python web framework
- Pydantic - Data validation
- Google Generative AI - AI-powered advice
- CORS - Cross-origin requests

### Frontend
- React 18 - UI library
- TypeScript - Type-safe code
- Vite - Lightning-fast build tool
- Recharts - Data visualization
- Lucide React - Icon library

## 🤝 Contributing

Improvements and suggestions are welcome! Areas for enhancement:
- Database integration for user accounts
- Historical tracking and trends
- Multi-currency support
- Investment portfolio optimization
- Tax planning features

## 📄 License

MIT License - feel free to use this project!

## 🆘 Support

For issues or questions:
1. Check the backend logs: `python -m uvicorn main:app --log-level debug`
2. Check browser console for frontend errors
3. Ensure API is running on port 8000
4. Verify CORS settings are correct

## 🚦 Troubleshooting

### API Connection Issues
- Ensure backend is running: `http://localhost:8000/health`
- Check CORS configuration in `main.py`
- Verify frontend `.env` has correct `VITE_API_URL`

### AI Features Not Working
- Verify `GEMINI_API_KEY` is set in backend `.env`
- Check API key validity at Google's console
- Review API usage limits

### UI Not Displaying
- Clear browser cache
- Check console for JavaScript errors
- Verify Recharts is properly installed: `npm list recharts`

---

**Made with ❤️ for better financial planning**

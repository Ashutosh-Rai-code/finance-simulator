# Development Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn
- Git

## Quick Start (One Command)

### Using Docker Compose (Recommended)

```bash
docker-compose up
```

This will start both backend and frontend automatically.

---

## Manual Setup

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo GEMINI_API_KEY=your_key_here > .env

# Run development server
python -m uvicorn main:app --reload
```

Server will be available at: `http://localhost:8000`

### 2. Frontend Setup

In a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
echo VITE_API_URL=http://localhost:8000/api > .env.local

# Start development server
npm run dev
```

App will be available at: `http://localhost:3000`

---

## Project Structure

```
finance_simulator/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── models.py            # Pydantic models
│   ├── services.py          # Business logic
│   ├── routes/              # API endpoints
│   ├── requirements.txt
│   ├── .env                 # Environment variables
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API clients
│   │   ├── App.tsx         # Root component
│   │   └── main.tsx        # Entry point
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── .env.local
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## Environment Configuration

### Backend (.env)

```env
GEMINI_API_KEY=your_gemini_api_key_here
FRONTEND_URL=http://localhost:3000
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

### Frontend (.env.local)

```env
VITE_API_URL=http://localhost:8000/api
```

---

## Common Commands

### Backend

```bash
cd backend

# Install new package
pip install package_name

# Update requirements
pip freeze > requirements.txt

# Run tests (if added)
pytest

# Format code
black .

# Lint
flake8 .
```

### Frontend

```bash
cd frontend

# Install new package
npm install package_name

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

---

## Debugging

### Backend Debug Mode

```bash
python -m uvicorn main:app --reload --log-level debug
```

Check `http://localhost:8000/docs` for interactive API docs (Swagger UI)

### Frontend Debug Mode

Open browser DevTools:
- `F12` or `Ctrl+Shift+I` (Windows/Linux)
- `Cmd+Option+I` (macOS)

Check console and network tabs for errors.

---

## Testing the API

### Using cURL

```bash
# Test health endpoint
curl http://localhost:8000/health

# Calculate metrics
curl -X POST http://localhost:8000/api/financial/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "income": 100000,
    "expenses": 50000,
    "savings": 500000,
    "sip": 20000,
    "target_goal": 1000000
  }'
```

### Using Postman

1. Import `backend/main.py` endpoints
2. Set base URL: `http://localhost:8000`
3. Add request body with financial data
4. Send requests

---

## Deployment

### Heroku

1. Create Procfile in backend:
   ```
   web: gunicorn main:app --worker-class uvicorn.workers.UvicornWorker
   ```

2. Deploy:
   ```bash
   git push heroku main
   ```

### AWS / Google Cloud

Use docker-compose for containerized deployment.

---

## Features

### Current (v2.0)
- ✅ Financial metrics calculation
- ✅ Risk analysis
- ✅ Wealth roadmap visualization
- ✅ What-if simulator
- ✅ AI financial coach
- ✅ Quit job analysis
- ✅ Modern responsive UI

### Planned
- 📋 User accounts & authentication
- 💾 Database integration
- 📊 Historical tracking
- 🌍 Multi-currency support
- 💼 Portfolio optimization
- 🎓 Financial education module

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>

# Or use different port
python -m uvicorn main:app --port 8001
```

### CORS Errors

Ensure `FRONTEND_URL` in backend `.env` matches your frontend URL.

### Module Not Found

```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
npm ci
```

### API Not Responding

1. Check if backend is running: `http://localhost:8000/health`
2. Check if frontend can reach backend URL
3. Check browser DevTools Network tab
4. Check backend console for errors

---

## Support

For help:
1. Check the main README.md
2. Review API docs at `http://localhost:8000/docs`
3. Check console/terminal for error messages
4. Review `.env` files for configuration issues

---

**Happy coding! 🚀**

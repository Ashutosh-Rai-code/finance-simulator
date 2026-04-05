# Project Structure Overview

## Complete Directory Tree

```
finance_simulator/
│
├── backend/                           # FastAPI Backend
│   ├── main.py                        # FastAPI application entrypoint
│   ├── models.py                      # Pydantic data models
│   ├── services.py                    # Financial & AI services
│   ├── routes/                        # API route handlers
│   │   ├── __init__.py
│   │   ├── financial.py               # Financial calculation APIs
│   │   └── ai_coach.py                # AI advisor APIs
│   ├── requirements.txt               # Python dependencies
│   ├── .env                           # Environment variables (TEMPLATE)
│   ├── Dockerfile                     # Container image
│   └── models/                        # (Reserved for future data models)
│       └── __init__.py
│
├── frontend/                          # React + TypeScript Frontend
│   ├── public/                        # Static assets (if needed)
│   ├── src/
│   │   ├── components/                # Reusable UI components
│   │   │   ├── Sidebar.tsx            # Navigation sidebar
│   │   │   ├── Sidebar.css
│   │   │   ├── MetricsCard.tsx        # Financial metric display
│   │   │   ├── MetricsCard.css
│   │   │   ├── ProgressBar.tsx        # Goal progress indicator
│   │   │   ├── ProgressBar.css
│   │   │   ├── RiskCard.tsx           # Risk analysis display
│   │   │   ├── RiskCard.css
│   │   │   ├── InputPanel.tsx         # Financial input sliders
│   │   │   ├── InputPanel.css
│   │   │   ├── RoadmapChart.tsx       # Wealth roadmap visualization
│   │   │   ├── RoadmapChart.css
│   │   │   ├── WhatIfSimulator.tsx    # Scenario simulator
│   │   │   ├── WhatIfSimulator.css
│   │   │   ├── AICoachPanel.tsx       # AI advice display
│   │   │   └── AICoachPanel.css
│   │   │
│   │   ├── pages/                     # Page-level components
│   │   │   ├── Dashboard.tsx          # Main dashboard page
│   │   │   ├── Dashboard.css
│   │   │   ├── QuitJobPage.tsx        # Quit job analysis page
│   │   │   └── QuitJobPage.css
│   │   │
│   │   ├── services/                  # API & utility services
│   │   │   └── api.ts                 # API client service
│   │   │
│   │   ├── styles/                    # Global styles (if separated)
│   │   │   └── (future use)
│   │   │
│   │   ├── hooks/                     # Custom React hooks (if needed)
│   │   │   └── (future use)
│   │   │
│   │   ├── App.tsx                    # Root component
│   │   ├── App.css                    # Root styles
│   │   ├── main.tsx                   # React entry point
│   │   └── index.css                  # Global CSS variables
│   │
│   ├── index.html                     # HTML template
│   ├── package.json                   # Node dependencies
│   ├── package-lock.json              # Locked versions
│   ├── vite.config.ts                 # Vite configuration
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── tsconfig.node.json             # TypeScript node config
│   ├── .env.example                   # Environment template
│   ├── .env.local                     # Environment variables (LOCAL)
│   └── Dockerfile                     # Container image
│
├── docker-compose.yml                 # Multi-container orchestration
├── .gitignore                         # Git ignore rules
│
├── README.md                          # Main documentation
├── DEVELOPMENT.md                     # Development setup guide
├── SETUP_COMPLETE.md                  # Completion summary
├── PROJECT_STRUCTURE.md               # This file
│
└── (Original Streamlit files)
    ├── app.py
    ├── app_first.py
    ├── app_second.py
    ├── app_third.py
    ├── app_fourth.py
    ├── app_fifth.py
    ├── app_sixth.py
    └── Untitled-1.ipynb
```

---

## Component Responsibilities

### Backend Components

**main.py**
- FastAPI application setup
- CORS configuration
- Route registration
- Health check endpoints

**models.py**
- FinancialInput - User financial data
- Metrics - Calculated metrics
- Risk - Risk information
- RoadmapData - Wealth projection data
- AICoachResponse - AI advice structure
- Snapshot - Historical data point

**services.py**
- FinancialCalculator class
  - calculate_metrics()
  - analyze_risks()
  - generate_roadmap()
  - calculate_goal_progress()
- AICoachService class
  - get_personalized_advice()
  - analyze_quit_job()

**routes/financial.py**
- /metrics endpoint
- /risks endpoint
- /roadmap endpoint
- /goal-progress endpoint
- /what-if endpoint

**routes/ai_coach.py**
- /advice endpoint
- /quit-job-analysis endpoint

---

### Frontend Components

**Sidebar**
- Navigation menu
- Page routing
- Responsive drawer

**MetricsCard**
- Displays single metric
- Shows trends (up/down/neutral)
- Interactive hover effects

**ProgressBar**
- Visual goal tracking
- Percentage display
- Remaining amount

**RiskCard**
- Lists financial risks
- Severity indicators
- Recommendations

**InputPanel**
- Range sliders for 5 inputs
- Real-time value display
- Triggers API calls

**RoadmapChart**
- Area chart visualization
- Data table below chart
- Milestone highlighting

**WhatIfSimulator**
- SIP adjustment slider
- Comparison display
- Additional wealth calculation

**AICoachPanel**
- Immediate actions section
- 90-day plan section
- 1-year vision section
- Loading state

**Dashboard**
- Orchestrates all components
- Manages state
- API data fetching
- Error handling

**QuitJobPage**
- Financial readiness analysis
- Risk assessment
- Recommendations
- Metric calculations

---

## Data Flow

### User Input → Calculation → Visualization

```
User adjusts sliders (InputPanel)
            ↓
[onChange event fires]
            ↓
State updates in Dashboard
            ↓
API call to backend
            ↓
Backend calculates metrics, risks, roadmap
            ↓
Response returns to frontend
            ↓
Dashboard state updates
            ↓
Components re-render with new data
            ↓
User sees updated dashboard
```

---

## API Communication

### RESTful Endpoints

**Financial Calculations** (POST requests)
- Request: JSON with income, expenses, savings, sip, target_goal
- Response: JSON with calculated metrics
- Used by: MetricsCard, ProgressBar, RiskCard

**AI Integration** (POST requests)
- Request: JSON financial data
- Response: JSON with advice sections
- Used by: AICoachPanel

**Risk Analysis** (POST request)
- Request: JSON financial data
- Response: JSON array of risks
- Used by: RiskCard

**Roadmap Generation** (POST request)
- Request: JSON with savings and sip
- Response: JSON array of yearly projections
- Used by: RoadmapChart

---

## State Management

### Frontend State
```javascript
// Dashboard.tsx
const [data, setData] = useState<FinancialData>({ ... })
const [metrics, setMetrics] = useState<Metrics | null>()
const [risks, setRisks] = useState<any[]>([])
const [roadmap, setRoadmap] = useState<any[]>([])
const [loading, setLoading] = useState(false)

// App.tsx (top level)
const [theme, setTheme] = useState<'light' | 'dark'>('dark')
const [currentPage, setCurrentPage] = useState<MenuItem>('dashboard')
const [sidebarOpen, setSidebarOpen] = useState(true)
```

All state is managed at component level using React hooks.

---

## Styling System

### CSS Variables (Dark Theme Default)
```css
--primary: #10b981 (green)
--primary-dark: #059669 (darker green)
--secondary: #8b5cf6 (purple)
--background: #0f172a (dark blue)
--surface: #1e293b (lighter dark)
--surface-light: #334155 (even lighter)
--text: #f1f5f9 (light text)
--text-muted: #cbd5e1 (muted text)
--danger: #ef4444 (red)
--warning: #f59e0b (orange)
--success: #10b981 (green)
--border: #475569 (border color)
```

### Responsive Breakpoints
- Mobile: < 768px (single column layout)
- Tablet: 768px - 1024px (optimized grid)
- Desktop: > 1024px (full features)

---

## Installation & Dependencies

### Backend Requirements
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
google-generativeai==0.3.0
python-multipart==0.0.6
```

### Frontend Dependencies
```
react: ^18.2.0
react-dom: ^18.2.0
axios: ^1.6.2
recharts: ^2.10.3
lucide-react: ^0.292.0
```

---

## Environment Configuration

### Backend .env
```
GEMINI_API_KEY=your_key_here
FRONTEND_URL=http://localhost:3000
```

### Frontend .env.local
```
VITE_API_URL=http://localhost:8000/api
```

---

## Build & Deployment

### Development
```bash
# Backend: http://localhost:8000
python -m uvicorn main:app --reload

# Frontend: http://localhost:3000
npm run dev
```

### Production
```bash
# Backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Frontend
npm run build  # Creates dist/ folder
npm run preview  # Preview build
```

### Docker
```bash
docker-compose up  # Builds and runs both
```

---

## File Counts Summary

| Directory | Files | Type |
|-----------|-------|------|
| backend | 9+ | Python/Config |
| frontend/src/components | 16 | TSX/CSS |
| frontend/src/pages | 4 | TSX/CSS |
| frontend/src | 6 | Config |
| frontend root | 7 | Config |
| Root | 5 | Config/Docs |
| **TOTAL** | **52+** | Mixed |

---

## Development Workflow

1. **Local Development**
   - Run backend and frontend separately
   - Use hot reload for changes
   - Test API with DevTools

2. **Testing**
   - Frontend: Browser DevTools
   - Backend: Swagger UI at /docs

3. **Deployment**
   - Use docker-compose
   - Or deploy to cloud platforms
   - Set production environment variables

---

## Future Enhancements

- [ ] Database integration (PostgreSQL)
- [ ] User authentication (JWT)
- [ ] Historical data tracking
- [ ] Multi-currency support
- [ ] Advanced charts (Portfolio breakdown)
- [ ] Export to PDF
- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] Investment recommendations
- [ ] Tax planning features

---

**This architecture provides a solid foundation for a professional, scalable financial planning application.**

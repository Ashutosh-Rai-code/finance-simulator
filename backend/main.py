from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from routes.financial import router as financial_router
from routes.ai_coach import router as ai_coach_router
from routes.visitor import router as visitor_router

# Create FastAPI app
app = FastAPI(
    title="AI Financial Coach API",
    description="Modern financial planning with AI",
    version="2.0.0"
)

# Configure CORS for React frontend - allow both HTTP and HTTPS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000").strip()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    frontend_url,
]

# If frontend_url is HTTP, also add HTTPS version for production
if frontend_url and frontend_url.startswith("http://") and "localhost" not in frontend_url:
    origins.append(frontend_url.replace("http://", "https://"))

# If frontend_url is HTTPS, also try HTTP for debugging
if frontend_url and frontend_url.startswith("https://"):
    # For production HTTPS URLs, also add the plain domain
    origins.append(frontend_url)

# Remove duplicates while preserving order
origins = list(dict.fromkeys(origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(financial_router)
app.include_router(ai_coach_router)
app.include_router(visitor_router)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "message": "AI Financial Coach API",
        "status": "running",
        "version": "2.0.0"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

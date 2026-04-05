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

# Configure CORS for React frontend
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    os.getenv("FRONTEND_URL", "http://localhost:3000")
]

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

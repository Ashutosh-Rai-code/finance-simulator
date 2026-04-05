from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services import AICoachService

router = APIRouter(prefix="/api/ai", tags=["ai"])

ai_service = AICoachService()


class AICoachInput(BaseModel):
    income: float
    expenses: float
    savings: float
    sip: float
    execute_ai: bool = False


class QuitJobAnalysisInput(BaseModel):
    savings: float = 0
    expenses: float = 0
    execute_ai: bool = False


@router.post("/advice")
def get_ai_advice(data: AICoachInput):
    """Get personalized AI financial advice"""
    try:
        advice = ai_service.get_personalized_advice(
            data.income,
            data.expenses,
            data.savings,
            data.sip,
            execute_ai=data.execute_ai,
        )
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quit-job-analysis")
def analyze_quit_job(data: QuitJobAnalysisInput):
    """Analyze if user can quit job"""
    try:
        analysis = ai_service.analyze_quit_job(
            data.savings,
            data.expenses,
            execute_ai=data.execute_ai,
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

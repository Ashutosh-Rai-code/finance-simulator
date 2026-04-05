from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FinancialInput(BaseModel):
    income: float
    expenses: float
    savings: float
    sip: float
    target_goal: float = 1000000


class UserProfile(BaseModel):
    income: float
    expenses: float
    savings: float
    sip: float
    target_goal: float
    created_at: datetime = datetime.now()


class Snapshot(BaseModel):
    time: datetime
    income: float
    expenses: float
    savings: float
    sip: float


class Metrics(BaseModel):
    savings_rate: float
    emergency_months: float
    sip_ratio: float
    monthly_surplus: float
    goal_progress: float


class Risk(BaseModel):
    risk: str
    recommendation: str
    severity: str  # "low", "medium", "high"


class RiskAnalysis(BaseModel):
    risks: List[Risk]


class RoadmapData(BaseModel):
    year: int
    value_in_lakhs: float
    notes: str


class AICoachResponse(BaseModel):
    current_metrics: dict
    action_plan: List[dict]
    roadmap: List[RoadmapData]

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FinancialInput(BaseModel):
    income: float
    expenses: float
    savings: float
    sip: float
    target_goal: float = 1000000


class WhatIfInput(BaseModel):
    income: float
    expenses: float
    savings: float
    sip: float
    target_goal: float = 1000000
    new_sip: float
    rate_of_return: float = 0.12
    duration_years: int = 10


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
    savings: float
    investments: float
    net_worth: float
    milestones: List[str]


class GoalProgress(BaseModel):
    current_amount: float
    target_amount: float
    progress_percentage: float
    time_to_goal_years: float
    projected_completion_date: str


class WhatIfResult(BaseModel):
    new_sip: float
    time_to_goal_years: float
    total_invested: float
    projected_value: float
    savings: List[float]


class AIAdvice(BaseModel):
    immediate_actions: List[str]
    ninety_day_plan: List[str]
    one_year_vision: str


class QuitJobAnalysis(BaseModel):
    survival_months: float
    risk_level: str
    advice: str
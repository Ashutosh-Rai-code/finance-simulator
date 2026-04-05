from fastapi import APIRouter, HTTPException
from models import FinancialInput, Metrics, RiskAnalysis, Risk, WhatIfInput
from services import FinancialCalculator

router = APIRouter(prefix="/api/financial", tags=["financial"])

calculator = FinancialCalculator()


@router.post("/metrics", response_model=Metrics)
def calculate_metrics(data: FinancialInput):
    """Calculate financial metrics"""
    try:
        metrics = calculator.calculate_metrics(
            data.income, 
            data.expenses, 
            data.savings, 
            data.sip
        )
        
        goal_progress = calculator.calculate_goal_progress(
            data.savings, 
            data.target_goal
        )
        
        return Metrics(
            savings_rate=metrics["savings_rate"],
            emergency_months=metrics["emergency_months"],
            sip_ratio=metrics["sip_ratio"],
            monthly_surplus=metrics["monthly_surplus"],
            goal_progress=goal_progress
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/risks", response_model=RiskAnalysis)
def analyze_risks(data: FinancialInput):
    """Analyze financial risks"""
    try:
        metrics = calculator.calculate_metrics(
            data.income, 
            data.expenses, 
            data.savings, 
            data.sip
        )
        
        risks = calculator.analyze_risks(
            data.income,
            data.expenses,
            data.savings,
            data.sip,
            metrics["savings_rate"] / 100,
            metrics["emergency_months"],
            metrics["sip_ratio"] / 100
        )
        
        return RiskAnalysis(
            risks=[Risk(**risk) for risk in risks]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/roadmap")
def get_roadmap(data: FinancialInput):
    """Get wealth roadmap to 1Cr"""
    try:
        roadmap = calculator.generate_roadmap(
            data.savings,
            data.sip
        )
        return {"roadmap": roadmap}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/goal-progress")
def calculate_progress(data: FinancialInput):
    """Calculate progress towards goal"""
    try:
        progress = calculator.calculate_goal_progress(
            data.savings,
            data.target_goal
        )
        return {
            "current_savings": data.savings,
            "target_goal": data.target_goal,
            "progress_percentage": progress,
            "remaining": data.target_goal - data.savings
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/what-if")
def what_if_simulation(data: WhatIfInput):
    """Simulate what-if scenarios with different SIP amounts"""
    try:
        rate = data.rate_of_return
        if rate > 1:
            rate = rate / 100

        duration = max(1, data.duration_years)

        current_roadmap = calculator.generate_roadmap(data.savings, data.sip, rate, duration)
        new_roadmap = calculator.generate_roadmap(data.savings, data.new_sip, rate, duration)
        
        current_final = current_roadmap[-1]["value_rupees"]
        new_final = new_roadmap[-1]["value_rupees"]
        difference = new_final - current_final
        
        return {
            "current_roadmap": current_roadmap,
            "new_roadmap": new_roadmap,
            "current_final_value": current_final,
            "new_final_value": new_final,
            "additional_wealth": difference,
            "rate_of_return": rate,
            "duration_years": duration
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "AI Financial Coach API" in response.json()["message"]

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_financial_metrics():
    test_data = {
        "income": 100000,
        "expenses": 50000,
        "savings": 200000,
        "sip": 10000,
        "target_goal": 1000000
    }
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/api/financial/metrics", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "savings_rate" in data
        assert "emergency_months" in data
        assert "sip_ratio" in data
        assert "monthly_surplus" in data
        assert "goal_progress" in data

@pytest.mark.asyncio
async def test_financial_risks():
    test_data = {
        "income": 100000,
        "expenses": 50000,
        "savings": 200000,
        "sip": 10000,
        "target_goal": 1000000
    }
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/api/financial/risks", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "risks" in data
        assert isinstance(data["risks"], list)

@pytest.mark.asyncio
async def test_financial_roadmap():
    test_data = {
        "income": 100000,
        "expenses": 50000,
        "savings": 200000,
        "sip": 10000,
        "target_goal": 1000000
    }
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/api/financial/roadmap", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "roadmap" in data
        assert isinstance(data["roadmap"], list)
        assert len(data["roadmap"]) > 0

@pytest.mark.asyncio
async def test_what_if_simulation():
    test_data = {
        "income": 100000,
        "expenses": 50000,
        "savings": 200000,
        "sip": 10000,
        "target_goal": 1000000,
        "new_sip": 15000,
        "rate_of_return": 0.12,
        "duration_years": 10
    }
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/api/financial/what-if", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "current_roadmap" in data
        assert "new_roadmap" in data
        assert "additional_wealth" in data

@pytest.mark.asyncio
async def test_ai_advice():
    test_data = {
        "income": 100000,
        "expenses": 50000,
        "savings": 200000,
        "sip": 10000
    }
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/api/ai/advice", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "immediate_actions" in data
        assert "ninety_day_plan" in data
        assert "one_year_vision" in data

@pytest.mark.asyncio
async def test_quit_job_analysis():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/api/ai/quit-job-analysis?savings=200000&expenses=50000")
        assert response.status_code == 200
        data = response.json()
        assert "survival_months" in data
        assert "risk_level" in data
        assert "advice" in data
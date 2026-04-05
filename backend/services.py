import google.generativeai as genai
import json
import os
import threading
from pathlib import Path
from typing import Dict, List, Tuple
import re

VISITOR_STORE_PATH = Path(__file__).resolve().parent / 'visitor_count.json'
VISITOR_LOCK = threading.Lock()


class FinancialCalculator:
    """Core financial calculation engine"""
    
    @staticmethod
    def calculate_metrics(income: float, expenses: float, savings: float, sip: float) -> Dict:
        """Calculate key financial metrics"""
        savings_rate = (income - expenses) / income if income > 0 else 0
        emergency_months = savings / expenses if expenses > 0 else 0
        sip_ratio = sip / income if income > 0 else 0
        monthly_surplus = income - expenses
        
        return {
            "savings_rate": round(savings_rate * 100, 2),
            "emergency_months": round(emergency_months, 1),
            "sip_ratio": round(sip_ratio * 100, 2),
            "monthly_surplus": round(monthly_surplus, 0)
        }
    
    @staticmethod
    def analyze_risks(income: float, expenses: float, savings: float, 
                      sip: float, savings_rate: float, emergency_months: float, 
                      sip_ratio: float) -> List[Dict]:
        """Generate risk analysis with recommendations"""
        risks = []
        
        if savings_rate < 20:
            risks.append({
                "risk": "Low savings rate",
                "recommendation": "Increase savings to 30%+",
                "severity": "high"
            })
        
        if emergency_months < 3:
            risks.append({
                "risk": "Weak emergency fund",
                "recommendation": "Build 6 months buffer (₹{:,.0f})".format(expenses * 6 / 100000),
                "severity": "high"
            })
        
        if sip_ratio < 10:
            risks.append({
                "risk": "Low investment allocation",
                "recommendation": "Increase SIP to 20% of income",
                "severity": "medium"
            })
        
        if expenses > 0.7 * income:
            risks.append({
                "risk": "High expense ratio",
                "recommendation": "Cut discretionary spend by 10-20%",
                "severity": "medium"
            })
        
        if emergency_months > 12:
            risks.append({
                "risk": "Over-saving in liquid assets",
                "recommendation": "Allocate excess to long-term investments",
                "severity": "low"
            })
        
        return risks
    
    @staticmethod
    def generate_roadmap(current_savings: float, sip: float, 
                        rate: float = 0.12, years: int = 10) -> List[Dict]:
        """Generate wealth roadmap for the chosen duration"""
        data = []
        value = current_savings
        
        for y in range(1, years + 1):
            yearly_investment = sip * 12
            value = (value + yearly_investment) * (1 + rate)
            
            data.append({
                "year": 2025 + y,
                "value_in_lakhs": round(value / 100000, 1),
                "value_rupees": round(value, 0),
                "notes": "Starting phase" if y <= 2 else "Growth phase" if y <= 5 else "Compound phase"
            })
        
        return data
    
    @staticmethod
    def calculate_goal_progress(current_savings: float, goal: float) -> float:
        """Calculate progress towards goal"""
        if goal <= 0:
            return 0
        return min((current_savings / goal) * 100, 100)


class VisitorCounter:
    def __init__(self, path: Path = VISITOR_STORE_PATH):
        self.path = path
        self._ensure_file()

    def _ensure_file(self):
        if not self.path.exists():
            self._write_data({"unique_visitors": [], "count": 0})

    def _read_data(self) -> dict:
        try:
            with self.path.open('r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except Exception:
            return {"unique_visitors": [], "count": 0}

    def _write_data(self, data: dict):
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(data, f)

    def get_count(self) -> int:
        with VISITOR_LOCK:
            data = self._read_data()
            return int(data.get('count', 0))

    def register_visitor(self, visitor_id: str) -> int:
        """Register a unique visitor (by IP or session ID). Returns updated count."""
        with VISITOR_LOCK:
            data = self._read_data()
            unique_visitors = data.get("unique_visitors", [])
            
            # Only increment if this visitor_id is new
            if visitor_id not in unique_visitors:
                unique_visitors.append(visitor_id)
                count = len(unique_visitors)
                data["unique_visitors"] = unique_visitors
                data["count"] = count
                self._write_data(data)
                return count
            
            return int(data.get('count', 0))


class AICoachService:
    """AI Financial Coach using Gemini API"""
    
    def __init__(self, api_key: str = None, model_name: str = None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if model_name is None:
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        if api_key:
            genai.configure(api_key=api_key)
        self.api_key = api_key
        self.model_name = model_name
        self.ai_enabled = os.getenv("AI_API_ENABLED", "false").lower() in ("1", "true", "yes")
        self.model = genai.GenerativeModel(model_name) if api_key else None
    
    def get_personalized_advice(self, income: float, expenses: float, 
                                savings: float, sip: float, execute_ai: bool = False) -> Dict:
        """Get AI-powered personalized financial advice"""
        if not self.api_key or not self.ai_enabled or not execute_ai:
            return self._get_default_advice(income, expenses, savings, sip)

        try:
            if not self.model:
                return self._get_default_advice(income, expenses, savings, sip)

            prompt = f"""
You are a world-class financial advisor. Analyze this profile and provide structured advice:

PROFILE:
- Monthly Income: ₹{income:,.0f}
- Monthly Expenses: ₹{expenses:,.0f}
- Current Savings: ₹{savings:,.0f}
- Monthly SIP: ₹{sip:,.0f}

Provide EXACTLY 3 sections with specific, measurable actions. Use bullet points only:

IMMEDIATE ACTIONS (Next 30 days):
- Action 1
- Action 2
- Action 3

90-DAY PLAN:
- Action 1
- Action 2
- Action 3
- Action 4

1-YEAR TRANSFORMATION:
One sentence describing the financial state after 1 year.

Use ₹ and specific numbers. Be precise and actionable.
            """

            response = self.model.generate_content(prompt)
            text = response.text

            return {
                "immediate_actions": self._parse_section(text, "IMMEDIATE ACTIONS"),
                "ninety_day_plan": self._parse_section(text, "90-DAY PLAN"),
                "one_year_vision": self._parse_vision(text)
            }

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def _get_default_advice(income: float, expenses: float, savings: float, sip: float) -> Dict:
        return {
            "immediate_actions": [
                "Review monthly budget and reduce non-essential expenses.",
                "Increase savings by at least 10% of income over the next 30 days.",
                "Set up an automated SIP contribution for long-term growth."
            ],
            "ninety_day_plan": [
                "Build an emergency fund equal to 3-6 months of expenses.",
                "Track spending weekly and identify one category to cut.",
                "Move surplus cash into SIP and savings buckets.",
                "Review insurance and emergency preparedness."
            ],
            "one_year_vision": "You will have stronger monthly savings discipline and a healthier emergency fund."
        }

    def analyze_quit_job(self, savings: float, expenses: float, execute_ai: bool = False) -> Dict:
        """Analyze if user can quit job with given savings"""
        if not self.api_key or not self.ai_enabled or not execute_ai:
            months = savings / expenses if expenses > 0 else 0
            return {
                "survival_months": months,
                "risk_level": "high" if months < 6 else "medium" if months < 12 else "safe",
                "advice": "You have {:.1f} months of runway".format(months)
            }
        
        try:
            if not self.model:
                months = savings / expenses if expenses > 0 else 0
                return {
                    "survival_months": months,
                    "risk_level": "high" if months < 6 else "medium" if months < 12 else "safe",
                    "advice": "You have {:.1f} months of runway".format(months)
                }
            
            prompt = f"""
Given:
- Savings: ₹{savings:,.0f}
- Monthly Expenses: ₹{expenses:,.0f}

Analyze if this person can quit their job. Provide:

Risk Level: [HIGH/MEDIUM/LOW]
Survival Months: [NUMBER]
Monthly Runway: [NUMBER] months
Emergency Fund Status: [ADEQUATE/INADEQUATE]
Recommendation: [ONE SPECIFIC ACTION]
            """
            response = self.model.generate_content(prompt)
            return self._parse_quit_job_response(response.text)
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def _parse_section(text: str, section_name: str) -> List[str]:
        """Parse sections from AI response"""
        lines = text.split('\n')
        in_section = False
        items = []
        
        for line in lines:
            line = line.strip()
            if section_name in line.upper():
                in_section = True
                continue
            
            if in_section:
                if re.match(r'^[-•*]\s+', line):
                    items.append(re.sub(r'^[-•*]\s+', '', line).strip())
                elif re.match(r'^\d+[\.)]\s+', line):
                    items.append(re.sub(r'^\d+[\.)]\s+', '', line).strip())
                elif any(keyword in line.upper() for keyword in ["IMMEDIATE", "90-DAY", "1-YEAR", "TRANSFORMATION"]) and len(items) > 0:
                    break
        
        return items
    
    @staticmethod
    def _parse_vision(text: str) -> str:
        """Parse the 1-year vision from AI response"""
        lines = text.split('\n')
        in_section = False
        
        for line in lines:
            line = line.strip()
            if "1-YEAR TRANSFORMATION" in line.upper():
                in_section = True
                continue
            
            if in_section and line:
                return line
        
        return "Achieve financial stability and growth."
    
    @staticmethod
    def _parse_quit_job_response(text: str) -> Dict:
        """Parse quit job analysis response"""
        lines = text.split('\n')
        result = {}
        
        for line in lines:
            line = line.strip()
            if "Risk Level:" in line:
                result["risk_level"] = line.split(":")[-1].strip().lower().replace("**", "")
            elif "Survival Months:" in line:
                try:
                    result["survival_months"] = float(re.findall(r'\d+', line)[0])
                except:
                    result["survival_months"] = 0
            elif "Monthly Runway:" in line:
                try:
                    result["monthly_runway"] = float(re.findall(r'\d+', line)[0])
                except:
                    result["monthly_runway"] = 0
            elif "Emergency Fund Status:" in line:
                result["emergency_fund_status"] = line.split(":")[-1].strip().lower().replace("**", "")
            elif "Recommendation:" in line:
                result["advice"] = line.split(":")[-1].strip().replace("**", "")
        
        return result
    
    @staticmethod
    def _get_default_advice(income: float, expenses: float, savings: float, sip: float) -> Dict:
        """Default advice when API is not available"""
        return {
            "immediate_actions": [
                f"Save ₹{min(10000, income*0.1):,.0f} extra this month",
                f"Move ₹{(sip/2):,.0f} into high-yield savings",
                "Cancel or reduce one non-essential subscription"
            ],
            "ninety_day_plan": [
                f"Raise SIP to ₹{(sip*1.15):,.0f}",
                f"Build emergency fund to ₹{expenses*3:,.0f}",
                "Track monthly spending categories weekly",
                "Rebalance investments toward long-term growth"
            ],
            "one_year_vision": f"Emergency fund ₹{expenses*6:,.0f}, SIP ₹{(sip*1.15):,.0f}, clearer wealth trajectory"
        }

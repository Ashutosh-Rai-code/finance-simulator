import streamlit as st
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import google.generativeai as genai
import os

api_key = None

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart Finance Simulator", layout="wide")

# ---------------- SESSION ----------------
if "app_started" not in st.session_state:
    st.session_state.app_started = False

# ---------------- UTILS ----------------
def format_inr(amount):
    return f"₹{amount:,.0f}"

# ---------------- CORE LOGIC ----------------
def calculate_metrics(income, expenses, savings, sip):
    savings_rate = (income - expenses) / income if income else 0
    emergency_months = savings / expenses if expenses else 0
    sip_ratio = sip / income if income else 0
    return savings_rate, emergency_months, sip_ratio

def calculate_score(savings_rate, emergency_months, sip_ratio, income, expenses):
    score = 0
    score += 30 if savings_rate > 0.4 else 20 if savings_rate > 0.2 else 10
    score += 30 if emergency_months > 6 else 20 if emergency_months > 3 else 10
    score += 20 if 0.2 <= sip_ratio <= 0.4 else 10 if sip_ratio < 0.2 else 5
    score += 20 if expenses < 0.6 * income else 0
    return score

def generate_risks_and_recommendations(savings_rate, emergency_months, sip_ratio, income, expenses):
    risks = []
    recs = []

    if savings_rate < 0.2:
        risks.append("Low savings rate")
        recs.append("Increase savings to 30%+")

    if emergency_months < 3:
        risks.append("Weak emergency fund")
        recs.append("Build 6 months expense buffer")

    if sip_ratio < 0.1:
        risks.append("Low investment allocation")
        recs.append("Increase SIP to 20% of income")

    if expenses > 0.7 * income:
        risks.append("High expense ratio")
        recs.append("Cut discretionary expenses by 15%")

    return risks, recs

# ---------------- AI ENGINE ----------------
def get_ai_advice(income, expenses, savings, sip):

    if not api_key:
        return "⚠️ AI not configured"

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are a sharp financial advisor.

        Income: {income}
        Expenses: {expenses}
        Savings: {savings}
        SIP: {sip}

        Give:
        - Top 3 risks
        - Top 3 actionable recommendations
        - One bold move to accelerate wealth

        Keep it concise and practical.
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"AI error: {str(e)}"

def ai_quit_job_analysis(savings, expenses):

    if not api_key:
        return "⚠️ AI not configured"

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        Savings: {savings}
        Monthly expenses: {expenses}

        Evaluate if user can quit job.

        Provide:
        - Risk level
        - Survival duration
        - What must be fixed
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"AI error: {str(e)}"

# ---------------- UI ----------------
st.markdown("""
<style>
.card {
    background: linear-gradient(145deg, #111827, #1f2937);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.5);
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-6px) scale(1.02);
}
.big-number {
    font-size: 28px;
    font-weight: bold;
    color: #22C55E;
}
.label {
    font-size: 14px;
    color: #9CA3AF;
}
</style>
""", unsafe_allow_html=True)

def card(title, value):
    return f"""
    <div class="card">
        <div class="label">{title}</div>
        <div class="big-number">{value}</div>
    </div>
    """

# ---------------- LANDING ----------------
if not st.session_state.app_started:
    st.title("💰 Smart Financial Decision Simulator")
    st.write("Move from guessing → to making data-driven financial decisions.")

    if st.button("Start"):
        st.session_state.app_started = True
        st.rerun()

# ---------------- MAIN ----------------
else:

    # Sidebar
    st.sidebar.title("Inputs")
    income = st.sidebar.slider("Income", 10000, 500000, 100000, step=5000)
    expenses = st.sidebar.slider("Expenses", 5000, 300000, 50000, step=5000)
    savings = st.sidebar.slider("Savings", 0, 5000000, 500000, step=50000)
    sip = st.sidebar.slider("SIP", 0, 200000, 20000, step=5000)

    menu = st.sidebar.selectbox("Menu", [
        "Overview",
        "Goal Planning",
        "Retirement",
        "Quit Job",
        "Report"
    ])

    savings_rate, emergency_months, sip_ratio = calculate_metrics(income, expenses, savings, sip)

    # ---------------- OVERVIEW ----------------
    if menu == "Overview":

        st.header("📊 Overview")

        score = calculate_score(savings_rate, emergency_months, sip_ratio, income, expenses)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(card("Income", format_inr(income)), unsafe_allow_html=True)

        with col2:
            st.markdown(card("Expenses", format_inr(expenses)), unsafe_allow_html=True)

        with col3:
            st.markdown(card("Savings", format_inr(savings)), unsafe_allow_html=True)

        with col4:
            st.markdown(card("SIP", format_inr(sip)), unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="label">Financial Score</div>
            <div class="big-number">{score}/100</div>
        </div>
        """, unsafe_allow_html=True)

        risks, recs = generate_risks_and_recommendations(
            savings_rate, emergency_months, sip_ratio, income, expenses
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("⚠️ Risks")
            for r in risks:
                st.write(f"- {r}")

        with col2:
            st.subheader("✅ Recommendations")
            for r in recs:
                st.write(f"- {r}")

        st.subheader("🤖 AI Advisor")

        if st.button("Generate AI Advice"):
            advice = get_ai_advice(income, expenses, savings, sip)
            st.write(advice)

    # ---------------- GOAL ----------------
    elif menu == "Goal Planning":

        st.header("🎯 Goal Planning")

        goal = st.slider("Goal Amount", 100000, 10000000, 1000000, step=100000)
        years = st.slider("Years", 1, 30, 10)
        rate = st.slider("Return %", 5, 15, 10)

        r = rate / 100 / 12
        n = years * 12
        sip_required = goal * r / ((1 + r)**n - 1)

        st.metric("Required SIP", format_inr(sip_required))

    # ---------------- RETIREMENT ----------------
    elif menu == "Retirement":

        st.header("🧓 Retirement")

        expense = st.slider("Monthly Expense", 20000, 300000, 80000, step=5000)
        age = st.slider("Current Age", 22, 60, 35)
        retire_age = st.slider("Retirement Age", 50, 65, 60)
        rate = st.slider("Return %", 5, 15, 10)

        years = retire_age - age
        corpus = expense * 12 * 25

        r = rate / 100 / 12
        n = years * 12
        future = sip * ((1 + r)**n - 1) / r

        st.metric("Required Corpus", format_inr(corpus))
        st.metric("Projected Corpus", format_inr(future))

        fig, ax = plt.subplots()
        ax.plot([0, years], [savings, future])
        st.pyplot(fig)

    # ---------------- QUIT JOB ----------------
    elif menu == "Quit Job":

        st.header("🚪 Quit Job")

        months = savings / expenses if expenses else 0
        st.metric("Survival Months", f"{months:.1f}")

        if st.button("AI Decision Analysis"):
            result = ai_quit_job_analysis(savings, expenses)
            st.write(result)

    # ---------------- REPORT ----------------
    elif menu == "Report":

        st.header("📄 Report")

        def create_pdf():
            doc = SimpleDocTemplate("report.pdf")
            styles = getSampleStyleSheet()
            content = []

            content.append(Paragraph("Financial Report", styles['Title']))
            content.append(Spacer(1, 20))

            content.append(Paragraph(f"Income: {format_inr(income)}", styles['Normal']))
            content.append(Paragraph(f"Expenses: {format_inr(expenses)}", styles['Normal']))
            content.append(Paragraph(f"Savings: {format_inr(savings)}", styles['Normal']))
            content.append(Paragraph(f"SIP: {format_inr(sip)}", styles['Normal']))

            doc.build(content)

        if st.button("Generate PDF"):
            create_pdf()
            with open("report.pdf", "rb") as f:
                st.download_button("Download", f)
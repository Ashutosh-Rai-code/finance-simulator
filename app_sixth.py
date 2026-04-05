import streamlit as st
import matplotlib.pyplot as plt
import os
import google.generativeai as genai
from datetime import datetime
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Financial Coach", layout="wide")

# ---------------- API SETUP ----------------
api_key = None
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ---------------- SESSION ----------------
if "app_started" not in st.session_state:
    st.session_state.app_started = False

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "income": 0,
        "expenses": 0,
        "savings": 0,
        "sip": 0,
        "history": []
    }

if "goal" not in st.session_state:
    st.session_state.goal = 1000000

# ---------------- UTILS ----------------
def format_inr(x):
    return f"₹{x:,.0f}"

def card(title, value):
    return f"""
    <div class="card">
        <div class="label">{title}</div>
        <div class="big-number">{value}</div>
    </div>
    """
def to_lakhs(x):
    return f"{x/100000:.1f}L"

def markdown_to_df(md_text):
    lines = md_text.split("\n")
    table_lines = [l for l in lines if "|" in l]

    rows = [l.strip("|").split("|") for l in table_lines]
    rows = [[c.strip() for c in r] for r in rows]
    df = pd.DataFrame(rows[2:], columns=rows[0])
    return df
# ---------------- CSS ----------------
st.markdown("""
<style>
.card {
    background: linear-gradient(145deg, #111827, #1f2937);
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 15px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.5);
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

# ---------------- CORE LOGIC ----------------
def calculate_metrics(income, expenses, savings, sip):
    savings_rate = (income - expenses) / income if income else 0
    emergency_months = savings / expenses if expenses else 0
    sip_ratio = sip / income if income else 0
    return savings_rate, emergency_months, sip_ratio

def generate_risks(savings_rate, emergency_months, sip_ratio, income, expenses):
    risks, recs = [], []

    if savings_rate < 0.2:
        risks.append("Low savings rate")
        recs.append("Increase savings to 30%+")

    if emergency_months < 3:
        risks.append("Weak emergency fund")
        recs.append("Build 6 months buffer")

    if sip_ratio < 0.1:
        risks.append("Low investment allocation")
        recs.append("Increase SIP to 20%")

    if expenses > 0.7 * income:
        risks.append("High expense ratio")
        recs.append("Cut discretionary spend")

    return risks, recs

# ---------------- AI COACH ----------------
def get_ai_coach():
    if not api_key:
        return "⚠️ AI not configured"

    profile = st.session_state.user_profile
    history = profile["history"][-3:]

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are a financial decision engine.

        User Profile:
        Income: {profile['income']}
        Expenses: {profile['expenses']}
        Savings: ₹{to_lakhs(profile['savings'])}
        SIP: {profile['sip']}

        Respond ONLY in this exact table format:

        | Metric | Value | Insight |
        |--------|------|--------|
        | Savings Rate | <value in %> | <1 short line> |
        | Emergency Fund | <months> | <1 short line> |
        | Investment Ratio | <value in %> | <1 short line> |
        | Risk Score | <Low/Medium/High> | <1 short line> |
        | Monthly Gap | <₹ value> | <1 short line> |

        | Action | Amount | Impact |
        |--------|--------|--------|
        | Increase SIP | ₹X (in L) | <1 short line> |
        | Reduce Expenses | ₹X (in L) | <1 short line> |
        | Target Savings | ₹X (in L) | <1 short line> |

        Rules:
        - Use ₹ with L (Lakhs), e.g., ₹5.0L
        - No paragraphs
        - Keep insights under 8 words
        - Be precise, not generic
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI error: {str(e)}"

def ai_quit_job(savings, expenses):
    if not api_key:
        return "⚠️ AI not configured"

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        Savings: {savings}
        Expenses: {expenses}

        Evaluate quitting job.

        Output:
        - Risk level
        - Survival months
        - Advice
        """

        return model.generate_content(prompt).text

    except Exception as e:
        return f"AI error: {str(e)}"

# ---------------- LANDING ----------------
if not st.session_state.app_started:
    st.title("💰 AI Financial Coach")
    st.write("From confusion → to clarity → to control")

    if st.button("Start"):
        st.session_state.app_started = True
        st.rerun()

# ---------------- MAIN ----------------
else:



    menu = st.sidebar.selectbox("Menu", ["Overview", "Quit Job"])

    st.sidebar.markdown("---")
    
    # Sidebar Inputs
    st.sidebar.header("Inputs")
    income = st.sidebar.slider("Income", 10000, 500000, 100000, step=5000)
    expenses = st.sidebar.slider("Expenses", 5000, 300000, 50000, step=5000)
    savings = st.sidebar.slider("Savings", 0, 5000000, 500000, step=50000)
    sip = st.sidebar.slider("SIP", 0, 200000, 20000, step=5000)

    savings_rate, emergency_months, sip_ratio = calculate_metrics(income, expenses, savings, sip)

    st.sidebar.markdown("---")

    # Goal
    st.sidebar.header("🎯 Goal")

    goal = st.sidebar.slider(
        "Target Savings",
        min_value=500000,
        max_value=10000000,
        value=st.session_state.goal,
        step=100000
    )
    st.sidebar.markdown(f"### 🎯 Target: ₹{goal:,.0f}")

    st.session_state.goal = goal

        # Update profile
    st.session_state.user_profile.update({
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "sip": sip
    })


    # ---------------- OVERVIEW ----------------
    if menu == "Overview":

        st.header("📊 Overview")

        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(card("Income", format_inr(income)), unsafe_allow_html=True)
        col2.markdown(card("Expenses", format_inr(expenses)), unsafe_allow_html=True)
        col3.markdown(card("Savings", format_inr(savings)), unsafe_allow_html=True)
        col4.markdown(card("SIP", format_inr(sip)), unsafe_allow_html=True)

        # Risks
        risks, recs = generate_risks(savings_rate, emergency_months, sip_ratio, income, expenses)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("⚠️ Risks")
            for r in risks:
                st.write(f"- {r}")

        with col2:
            st.subheader("✅ Recommendations")
            for r in recs:
                st.write(f"- {r}")

        # Goal progress
        st.subheader("🎯 Goal Progress")
        progress = savings / goal if goal else 0
        st.progress(min(progress, 1.0))
        st.write(f"{progress*100:.1f}% of ₹{goal:,.0f}")

        # Save snapshot
        if st.button("📌 Save Snapshot"):

            snapshot = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "income": income,
                "expenses": expenses,
                "savings": savings,
                "sip": sip
            }

            st.session_state.user_profile["history"].append(snapshot)

            st.success(f"Snapshot saved at {snapshot['time']}")

        # Trend
        history = st.session_state.user_profile["history"]
        if history:
            st.subheader("📈 Progress Trend")
            import matplotlib.ticker as ticker

            values = [h["savings"] for h in history]
            labels = [h["time"].split(" ")[0] for h in history]

            

            fig, ax = plt.subplots()

            for i, v in enumerate(values):
                ax.text(i, v, f"{v/100000:.1f}L", ha='center', va='bottom')

            ax.plot(values, marker='o')

            # Convert Y-axis to Lakhs
            def format_lakhs(x, pos):
                return f"{x/100000:.1f}L"

            ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_lakhs))

            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=45)

            ax.set_title("Savings Trend (₹ Lakhs)")

            st.pyplot(fig)
        if len(history) >= 2:
            latest = history[-1]["savings"]
            prev = history[-2]["savings"]

            change = latest - prev

            if change > 0:
                st.success(f"↑ Savings increased by ₹{change}")
            elif change < 0:
                st.error(f"↓ Savings decreased by ₹{abs(change)}")
            else:
                st.info("No change in savings")
        # AI Coach
        st.subheader("🧠 AI Coach")

        if st.button("Get Advice"):
            advice = get_ai_coach()
           # st.markdown(advice)
            df = markdown_to_df(advice)
            st.dataframe(df)

    # ---------------- QUIT JOB ----------------
    elif menu == "Quit Job":

        st.header("🚪 Quit Job")

        months = savings / expenses if expenses else 0
        st.metric("Survival Months", f"{months:.1f}")

        if st.button("AI Analysis"):
            result = ai_quit_job(savings, expenses)
            st.markdown(f"<div class='card'>{result}</div>", unsafe_allow_html=True)
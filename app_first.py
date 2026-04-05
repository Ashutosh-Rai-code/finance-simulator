import streamlit as st
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Finance Simulator", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #F5F5F5;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Smart Financial Decision Simulator (India)")

st.divider()

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 💼 Income & Savings")
    income = st.slider("Monthly Income (₹)", 10000, 500000, 100000, step=5000)
    savings = st.slider("Total Savings (₹)", 0, 5000000, 500000, step=50000)

with col2:
    st.markdown("## 💸 Expenses & Investments")
    expenses = st.slider("Monthly Expenses (₹)", 5000, 300000, 50000, step=5000)
    sip = st.slider("Monthly SIP (₹)", 0, 200000, 20000, step=5000)

st.divider()

# ---------------- CORE CALCULATIONS ----------------
savings_rate = (income - expenses) / income if income > 0 else 0
emergency_months = savings / expenses if expenses > 0 else 0
sip_ratio = sip / income if income > 0 else 0

# ---------------- FINANCIAL HEALTH SCORE ----------------
score = 0

if savings_rate > 0.4:
    score += 30
elif savings_rate > 0.2:
    score += 20
else:
    score += 10

if emergency_months > 6:
    score += 30
elif emergency_months > 3:
    score += 20
else:
    score += 10

if 0.2 <= sip_ratio <= 0.4:
    score += 20
elif sip_ratio < 0.2:
    score += 10
else:
    score += 5

if expenses < 0.6 * income:
    score += 20

st.subheader(f"📊 Financial Health Score: {score}/100")

st.divider()

# ---------------- RISK FLAGS ----------------
st.subheader("⚠️ Risk Flags")

if emergency_months < 3:
    st.write("⚠️ Emergency fund too low (<3 months)")

if sip_ratio > 0.5:
    st.write("⚠️ Over-investing, liquidity risk")

if savings_rate < 0.2:
    st.write("⚠️ Low savings rate")

st.divider()

# ---------------- PERSONALIZED RECOMMENDATIONS ----------------
st.subheader("📌 Personalized Recommendations")

gap_emergency = max((6 * expenses) - savings, 0)

if emergency_months < 6:
    st.write(f"👉 You need ₹{gap_emergency:,.0f} more to reach 6 months emergency fund.")

if sip_ratio > 0.4:
    excess = sip - (0.4 * income)
    st.write(f"👉 Reduce SIP by approx ₹{excess:,.0f} to improve liquidity.")

if savings_rate < 0.3:
    needed = (0.3 * income) - (income - expenses)
    st.write(f"👉 Increase monthly savings by ₹{needed:,.0f} to reach 30% savings rate.")

st.divider()

# ---------------- GOAL PLANNING ----------------
st.markdown("## 🎯 Goal Planning")

goal_amount = st.slider("Target Goal Amount (₹)", 100000, 10000000, step=100000)
years = st.slider("Years to achieve goal", 1, 30, 10)
expected_return = st.slider("Expected Annual Return (%)", 5, 15, 10)

r = expected_return / 100 / 12
n = years * 12

sip_required = goal_amount * r / ((1 + r)**n - 1) if r > 0 else goal_amount / n

st.subheader("Goal Planning Result")

st.write(f"👉 Required SIP: ₹{sip_required:,.0f} per month")

if sip_required > sip:
    st.write(f"⚠️ Your current SIP is short by ₹{sip_required - sip:,.0f}")
else:
    st.write("✅ You are on track for this goal")

st.divider()

# ---------------- RETIREMENT PLANNING ----------------
st.markdown("## 🧓 Retirement Planning")

current_age = st.slider("Current Age", 22, 60, 35)
retirement_age = st.slider("Retirement Age", 50, 65, 60)
monthly_expense_future = st.slider("Expected Monthly Expense at Retirement (₹)", 50000, 200000, 80000, step=10000)

years_left = retirement_age - current_age
annual_expense = monthly_expense_future * 12

retirement_corpus = annual_expense * 25  # 25x rule

r = expected_return / 100 / 12
n = years_left * 12

future_value = sip * ((1 + r)**n - 1) / r if r > 0 else sip * n

st.subheader("Retirement Analysis")

st.write(f"Required Corpus: ₹{retirement_corpus:,.0f}")
st.write(f"Projected Corpus: ₹{future_value:,.0f}")

gap = retirement_corpus - future_value

if gap > 0:
    st.write(f"⚠️ Shortfall: ₹{gap:,.0f}")
else:
    st.write("✅ You are on track for retirement")

st.divider()

# ---------------- VISUALIZATION ----------------
st.subheader("📊 Savings vs Retirement Projection")

labels = ['Current Savings', 'Projected Corpus']
values = [savings, future_value]

fig, ax = plt.subplots()
ax.bar(labels, values)

st.pyplot(fig)
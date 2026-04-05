import streamlit as st
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Finance Simulator", layout="wide")

st.title("💰 Smart Financial Decision Simulator (India)")

# ---------------- SIDEBAR NAV ----------------
section = st.sidebar.radio("📂 Navigate", [
    "Overview",
    "Goal Planning",
    "Retirement Planning",
    "Quit Job Simulator",
    "Download Report"
])

# ---------------- INPUTS (GLOBAL) ----------------
st.sidebar.markdown("## 🔧 Inputs")

income = st.sidebar.slider("Monthly Income (₹)", 10000, 500000, 100000, step=5000)
expenses = st.sidebar.slider("Monthly Expenses (₹)", 5000, 300000, 50000, step=5000)
savings = st.sidebar.slider("Total Savings (₹)", 0, 5000000, 500000, step=50000)
sip = st.sidebar.slider("Monthly SIP (₹)", 0, 200000, 20000, step=5000)

# ---------------- CALCULATIONS ----------------
savings_rate = (income - expenses) / income if income else 0
emergency_months = savings / expenses if expenses else 0
sip_ratio = sip / income if income else 0

# ---------------- OVERVIEW ----------------
if section == "Overview":

    st.header("📊 Financial Overview")

    st.markdown(f"### 💼 Income: ₹{income:,}")
    st.markdown(f"### 💸 Expenses: ₹{expenses:,}")
    st.markdown(f"### 💰 Savings: ₹{savings:,}")
    st.markdown(f"### 📈 SIP: ₹{sip:,}")

    # Score
    score = 0
    score += 30 if savings_rate > 0.4 else 20 if savings_rate > 0.2 else 10
    score += 30 if emergency_months > 6 else 20 if emergency_months > 3 else 10
    score += 20 if 0.2 <= sip_ratio <= 0.4 else 10 if sip_ratio < 0.2 else 5
    score += 20 if expenses < 0.6 * income else 0

    st.subheader(f"📊 Score: {score}/100")

    st.subheader("⚠️ Risks")
    if emergency_months < 3:
        st.write("Low emergency fund")
    if sip_ratio > 0.5:
        st.write("Over-investing risk")
    if savings_rate < 0.2:
        st.write("Low savings rate")

    st.subheader("📌 Recommendations")

    if emergency_months < 6:
        st.write(f"Add ₹{(6*expenses - savings):,.0f} to emergency fund")

    if sip_ratio > 0.4:
        st.write(f"Reduce SIP by ₹{(sip - 0.4*income):,.0f}")

# ---------------- GOAL PLANNING ----------------
elif section == "Goal Planning":

    st.header("🎯 Goal Planning")

    goal_amount = st.slider("Target Goal Amount (₹)", 100000, 10000000, 1000000, step=100000)
    years = st.slider("Years", 1, 30, 10)
    expected_return = st.slider("Return %", 5, 15, 10)

    r = expected_return / 100 / 12
    n = years * 12

    sip_required = goal_amount * r / ((1 + r)**n - 1)

    st.subheader(f"Required SIP: ₹{sip_required:,.0f}")

# ---------------- RETIREMENT ----------------
elif section == "Retirement Planning":

    st.header("🧓 Retirement Planning")

    current_age = st.slider("Current Age", 22, 60, 35)
    retirement_age = st.slider("Retirement Age", 50, 65, 60)
    monthly_expense_future = st.slider("Monthly Expense at Retirement (₹)", 20000, 300000, 80000, step=5000)
    expected_return = st.slider("Return %", 5, 15, 10)

    years_left = retirement_age - current_age
    corpus_needed = monthly_expense_future * 12 * 25

    r = expected_return / 100 / 12
    n = years_left * 12

    future_value = sip * ((1 + r)**n - 1) / r

    st.subheader(f"Required Corpus: ₹{corpus_needed:,.0f}")
    st.subheader(f"Projected Corpus: ₹{future_value:,.0f}")

    # Chart
    fig, ax = plt.subplots()
    ax.bar(["Required", "Projected"], [corpus_needed, future_value])
    st.pyplot(fig)

# ---------------- QUIT JOB SIMULATOR ----------------
elif section == "Quit Job Simulator":

    st.header("🚪 Quit Job Simulator")

    monthly_expense = expenses
    current_savings = savings

    months_survival = current_savings / monthly_expense if monthly_expense else 0

    st.subheader(f"You can survive {months_survival:.1f} months without income")

    if months_survival < 6:
        st.write("⚠️ Risky to quit now")
    elif months_survival < 12:
        st.write("⚠️ Moderate risk")
    else:
        st.write("✅ Safer zone")

# ---------------- PDF DOWNLOAD ----------------
elif section == "Download Report":

    st.header("📄 Download Report")

    def create_pdf():
        doc = SimpleDocTemplate("report.pdf")
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("Financial Report", styles['Title']))
        content.append(Spacer(1, 12))

        content.append(Paragraph(f"Income: ₹{income}", styles['Normal']))
        content.append(Paragraph(f"Expenses: ₹{expenses}", styles['Normal']))
        content.append(Paragraph(f"Savings: ₹{savings}", styles['Normal']))
        content.append(Paragraph(f"SIP: ₹{sip}", styles['Normal']))

        doc.build(content)

    if st.button("Generate PDF"):
        create_pdf()
        with open("report.pdf", "rb") as f:
            st.download_button("Download", f, file_name="financial_report.pdf")
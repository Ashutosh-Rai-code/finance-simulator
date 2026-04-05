import streamlit as st
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Finance Simulator", layout="wide")

# ---------------- FORMAT FUNCTION ----------------
def format_inr(amount):
    return f"₹{amount:,.0f}"

# ---------------- NAVIGATION (MENU STYLE) ----------------
st.sidebar.title("📂 Menu")

menu = st.sidebar.selectbox(
    "Go to",
    ["Overview", "Goal Planning", "Retirement Planning", "Quit Job Simulator", "Download Report"]
)

# ---------------- INPUTS ----------------
st.sidebar.markdown("## 🔧 Inputs")

income = st.sidebar.slider("Monthly Income", 10000, 500000, 100000, step=5000)
expenses = st.sidebar.slider("Monthly Expenses", 5000, 300000, 50000, step=5000)
savings = st.sidebar.slider("Total Savings", 0, 5000000, 500000, step=50000)
sip = st.sidebar.slider("Monthly SIP", 0, 200000, 20000, step=5000)

# ---------------- CALCULATIONS ----------------
savings_rate = (income - expenses) / income if income else 0
emergency_months = savings / expenses if expenses else 0
sip_ratio = sip / income if income else 0

# ---------------- OVERVIEW ----------------
if menu == "Overview":

    st.title("📊 Financial Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### 💼 Income: {format_inr(income)}")
        st.markdown(f"### 💰 Savings: {format_inr(savings)}")

    with col2:
        st.markdown(f"### 💸 Expenses: {format_inr(expenses)}")
        st.markdown(f"### 📈 SIP: {format_inr(sip)}")

    score = 0
    score += 30 if savings_rate > 0.4 else 20 if savings_rate > 0.2 else 10
    score += 30 if emergency_months > 6 else 20 if emergency_months > 3 else 10
    score += 20 if 0.2 <= sip_ratio <= 0.4 else 10 if sip_ratio < 0.2 else 5
    score += 20 if expenses < 0.6 * income else 0

    st.subheader(f"Score: {score}/100")

# ---------------- GOAL ----------------
elif menu == "Goal Planning":

    st.title("🎯 Goal Planning")

    goal_amount = st.slider("Target Goal Amount", 100000, 10000000, 1000000, step=100000)
    st.markdown(f"### Target Goal Amount: {format_inr(goal_amount)}")

    years = st.slider("Years", 1, 30, 10)
    expected_return = st.slider("Return %", 5, 15, 10)

    r = expected_return / 100 / 12
    n = years * 12

    sip_required = goal_amount * r / ((1 + r)**n - 1)

    st.subheader(f"Required SIP: {format_inr(sip_required)}")

# ---------------- RETIREMENT ----------------
elif menu == "Retirement Planning":

    st.title("🧓 Retirement Planning")

    monthly_expense_future = st.slider("Monthly Expense at Retirement", 20000, 300000, 80000, step=5000)
    st.markdown(f"### Expected Monthly Expense: {format_inr(monthly_expense_future)}")

    current_age = st.slider("Current Age", 22, 60, 35)
    retirement_age = st.slider("Retirement Age", 50, 65, 60)
    expected_return = st.slider("Return %", 5, 15, 10)

    years_left = retirement_age - current_age
    corpus_needed = monthly_expense_future * 12 * 25

    r = expected_return / 100 / 12
    n = years_left * 12

    future_value = sip * ((1 + r)**n - 1) / r

    st.subheader(f"Required Corpus: {format_inr(corpus_needed)}")
    st.subheader(f"Projected Corpus: {format_inr(future_value)}")

    # Improved chart
    fig, ax = plt.subplots()
    ax.plot([0, years_left], [savings, future_value])
    ax.set_title("Growth Projection")
    st.pyplot(fig)

# ---------------- QUIT JOB ----------------
elif menu == "Quit Job Simulator":

    st.title("🚪 Quit Job Simulator")

    months_survival = savings / expenses if expenses else 0

    st.subheader(f"You can survive {months_survival:.1f} months")

# ---------------- PDF ----------------
elif menu == "Download Report":

    st.title("📄 Download Financial Report")

    def create_pdf():
        doc = SimpleDocTemplate("report.pdf")
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("Financial Summary", styles['Title']))
        content.append(Spacer(1, 20))

        content.append(Paragraph(f"Income: {format_inr(income)}", styles['Normal']))
        content.append(Paragraph(f"Expenses: {format_inr(expenses)}", styles['Normal']))
        content.append(Paragraph(f"Savings: {format_inr(savings)}", styles['Normal']))
        content.append(Paragraph(f"SIP: {format_inr(sip)}", styles['Normal']))

        content.append(Spacer(1, 20))
        content.append(Paragraph("Insights", styles['Heading2']))
        content.append(Spacer(1, 10))

        if emergency_months < 6:
            content.append(Paragraph("Increase emergency fund", styles['Normal']))

        if sip_ratio > 0.4:
            content.append(Paragraph("Reduce SIP to improve liquidity", styles['Normal']))

        doc.build(content)

    if st.button("Generate PDF"):
        create_pdf()
        with open("report.pdf", "rb") as f:
            st.download_button("Download Report", f, file_name="financial_report.pdf")
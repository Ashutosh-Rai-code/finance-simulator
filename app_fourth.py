import streamlit as st
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Finance Simulator", layout="wide")

# ---------------- SESSION STATE ----------------
if "app_started" not in st.session_state:
    st.session_state.app_started = False

# ---------------- FORMAT ----------------
def format_inr(amount):
    return f"₹{amount:,.0f}"

# ---------------- PREMIUM CSS ----------------
st.markdown("""
<style>
.main { background-color: #0B0F19; }

.block-container { padding-top: 2rem; }

.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px);
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

.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 20px;
}

.hero {
    text-align: center;
    padding: 80px 20px;
}

.hero-title {
    font-size: 42px;
    font-weight: bold;
}

.hero-sub {
    font-size: 18px;
    color: #9CA3AF;
}

.stButton button {
    background-color: #2563EB;
    color: white;
    border-radius: 10px;
    padding: 12px 24px;
}

section[data-testid="stSidebar"] {
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LANDING PAGE ----------------
if not st.session_state.app_started:

    st.markdown("""
    <div class="hero">
        <div class="hero-title">💰 Smart Financial Decision Simulator</div>
        <br>
        <div class="hero-sub">
        Make smarter decisions about investing, savings, and life choices.<br><br>
        Know if you're on track — or heading for trouble.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Simulation"):
        st.session_state.app_started = True
        st.rerun()

# ---------------- MAIN APP ----------------
else:

    # Sidebar Navigation
    st.sidebar.title("📂 Menu")
    menu = st.sidebar.selectbox(
        "Navigate",
        ["Overview", "Goal Planning", "Retirement Planning", "Quit Job Simulator", "Download Report"]
    )

    # Sidebar Inputs
    st.sidebar.markdown("## 🔧 Inputs")
    income = st.sidebar.slider("Monthly Income", 10000, 500000, 100000, step=5000)
    expenses = st.sidebar.slider("Monthly Expenses", 5000, 300000, 50000, step=5000)
    savings = st.sidebar.slider("Total Savings", 0, 5000000, 500000, step=50000)
    sip = st.sidebar.slider("Monthly SIP", 0, 200000, 20000, step=5000)

    # Calculations
    savings_rate = (income - expenses) / income if income else 0
    emergency_months = savings / expenses if expenses else 0
    sip_ratio = sip / income if income else 0

    # ---------------- OVERVIEW ----------------
    if menu == "Overview":

        st.markdown('<div class="section-title">📊 Financial Overview</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f'<div class="card"><div class="label">Income</div><div class="big-number">{format_inr(income)}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><div class="label">Expenses</div><div class="big-number">{format_inr(expenses)}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="card"><div class="label">Savings</div><div class="big-number">{format_inr(savings)}</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="card"><div class="label">SIP</div><div class="big-number">{format_inr(sip)}</div></div>', unsafe_allow_html=True)

        score = 0
        score += 30 if savings_rate > 0.4 else 20 if savings_rate > 0.2 else 10
        score += 30 if emergency_months > 6 else 20 if emergency_months > 3 else 10
        score += 20 if 0.2 <= sip_ratio <= 0.4 else 10 if sip_ratio < 0.2 else 5
        score += 20 if expenses < 0.6 * income else 0

        st.markdown(f'<div class="card"><div class="label">Financial Score</div><div class="big-number">{score}/100</div></div>', unsafe_allow_html=True)
        
    # ---------------- GOAL ----------------
    elif menu == "Goal Planning":

        st.markdown('<div class="section-title">🎯 Goal Planning</div>', unsafe_allow_html=True)

        goal_amount = st.slider("Target Goal Amount", 100000, 10000000, 1000000, step=100000)
        st.markdown(f"### {format_inr(goal_amount)}")

        years = st.slider("Years", 1, 30, 10)
        expected_return = st.slider("Return %", 5, 15, 10)

        r = expected_return / 100 / 12
        n = years * 12
        sip_required = goal_amount * r / ((1 + r)**n - 1)

        st.markdown(f'<div class="card"><div class="label">Required SIP</div><div class="big-number">{format_inr(sip_required)}</div></div>', unsafe_allow_html=True)

    # ---------------- RETIREMENT ----------------
    elif menu == "Retirement Planning":

        st.markdown('<div class="section-title">🧓 Retirement Planning</div>', unsafe_allow_html=True)

        monthly_expense_future = st.slider("Monthly Expense", 20000, 300000, 80000, step=5000)
        st.markdown(f"### {format_inr(monthly_expense_future)}")

        current_age = st.slider("Current Age", 22, 60, 35)
        retirement_age = st.slider("Retirement Age", 50, 65, 60)
        expected_return = st.slider("Return %", 5, 15, 10)

        years_left = retirement_age - current_age
        corpus_needed = monthly_expense_future * 12 * 25

        r = expected_return / 100 / 12
        n = years_left * 12
        future_value = sip * ((1 + r)**n - 1) / r

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'<div class="card"><div class="label">Required Corpus</div><div class="big-number">{format_inr(corpus_needed)}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><div class="label">Projected Corpus</div><div class="big-number">{format_inr(future_value)}</div></div>', unsafe_allow_html=True)

        fig, ax = plt.subplots()
        ax.plot([0, years_left], [savings, future_value], linewidth=3)
        ax.set_title("Wealth Growth")
        st.pyplot(fig)

    # ---------------- QUIT JOB ----------------
    elif menu == "Quit Job Simulator":

        st.markdown('<div class="section-title">🚪 Quit Job Simulator</div>', unsafe_allow_html=True)

        months = savings / expenses if expenses else 0

        color = "#EF4444" if months < 6 else "#F59E0B" if months < 12 else "#22C55E"

        st.markdown(f"""
        <div class="card">
            <div class="label">Survival Duration</div>
            <div class="big-number" style="color:{color}">
                {months:.1f} months
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- PDF ----------------
    elif menu == "Download Report":

        st.markdown('<div class="section-title">📄 Download Report</div>', unsafe_allow_html=True)

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
                st.download_button("Download", f, file_name="financial_report.pdf")
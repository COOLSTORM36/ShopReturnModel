import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Shop Business Model",
    page_icon="🍜",
    layout="wide"
)

st.title("🍜 Noodle Shop Business Model")
st.caption("Financial model for a small takeaway / delivery-focused noodle shop")

# ============================================================
# SIDEBAR — INPUTS
# ============================================================

st.sidebar.header("⚙️ Business Parameters")

# ============================================================
# 1. INITIAL INVESTMENT
# ============================================================

st.sidebar.subheader("💷 Initial Investment")

initial_investment = st.sidebar.number_input(
    "Initial Investment (£)",
    min_value=0.0,
    value=50000.0,
    step=1000.0,
    help="Total money invested before opening."
)

# ============================================================
# 2. SALES PARAMETERS
# ============================================================

st.sidebar.subheader("📈 Sales Parameters")

customers_per_day = st.sidebar.number_input(
    "Customers / Orders per Day",
    min_value=0,
    value=40,
    step=1
)

average_order_value = st.sidebar.number_input(
    "Average Order Value (£)",
    min_value=0.0,
    value=15.0,
    step=0.5
)

operating_days = st.sidebar.number_input(
    "Operating Days / Month",
    min_value=1,
    max_value=31,
    value=30,
    step=1
)

# ============================================================
# 3. VARIABLE COSTS
# ============================================================

st.sidebar.subheader("🥢 Variable Costs")

food_cost_per_order = st.sidebar.number_input(
    "Food Cost per Order (£)",
    min_value=0.0,
    value=4.0,
    step=0.5
)

packaging_cost_per_order = st.sidebar.number_input(
    "Packaging Cost per Order (£)",
    min_value=0.0,
    value=0.5,
    step=0.1
)

payment_fee_percent = st.sidebar.number_input(
    "Payment Processing Fee (%)",
    min_value=0.0,
    max_value=100.0,
    value=1.5,
    step=0.1
)

delivery_platform_percent = st.sidebar.number_input(
    "Delivery Platform Commission (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0,
    help="Set this to 0% if delivery platform commission is already included elsewhere."
)

# ============================================================
# 4. FIXED MONTHLY COSTS
# ============================================================

st.sidebar.subheader("🏪 Fixed Monthly Costs")

rent = st.sidebar.number_input(
    "Rent (£ / Month)",
    min_value=0.0,
    value=1500.0,
    step=100.0
)

num_employees = st.sidebar.number_input(
    "Number of Employees",
    min_value=0,
    value=3,
    step=1
)

salary_per_employee = st.sidebar.number_input(
    "Salary per Employee (£ / Month)",
    min_value=0.0,
    value=2700.0,
    step=100.0
)

utilities = st.sidebar.number_input(
    "Utilities (£ / Month)",
    min_value=0.0,
    value=250.0,
    step=50.0
)

other_fixed_costs = st.sidebar.number_input(
    "Other Fixed Costs (£ / Month)",
    min_value=0.0,
    value=350.0,
    step=50.0
)

# ============================================================
# 5. ANALYSIS PERIOD
# ============================================================

st.sidebar.subheader("📅 Analysis")

analysis_months = st.sidebar.slider(
    "Analysis Period (Months)",
    min_value=12,
    max_value=120,
    value=60,
    step=12
)

# ============================================================
# CALCULATIONS
# ============================================================

# ------------------------------------------------------------
# Employee cost
# ------------------------------------------------------------

employee_cost = (
    num_employees * salary_per_employee
)

# ------------------------------------------------------------
# Fixed monthly cost
# ------------------------------------------------------------

fixed_monthly_cost = (
    rent
    + employee_cost
    + utilities
    + other_fixed_costs
)

# ------------------------------------------------------------
# Monthly orders
# ------------------------------------------------------------

monthly_orders = (
    customers_per_day * operating_days
)

# ------------------------------------------------------------
# Monthly revenue
# ------------------------------------------------------------

monthly_revenue = (
    monthly_orders * average_order_value
)

# ------------------------------------------------------------
# Payment fee per order
# ------------------------------------------------------------

payment_fee_per_order = (
    average_order_value
    * payment_fee_percent
    / 100
)

# ------------------------------------------------------------
# Delivery platform fee per order
# ------------------------------------------------------------

delivery_fee_per_order = (
    average_order_value
    * delivery_platform_percent
    / 100
)

# ------------------------------------------------------------
# Total variable cost per order
# ------------------------------------------------------------

total_variable_cost_per_order = (
    food_cost_per_order
    + packaging_cost_per_order
    + payment_fee_per_order
    + delivery_fee_per_order
)

# ------------------------------------------------------------
# Contribution per order
# ------------------------------------------------------------

contribution_per_order = (
    average_order_value
    - total_variable_cost_per_order
)

# ------------------------------------------------------------
# Contribution margin
# ------------------------------------------------------------

if average_order_value > 0:

    contribution_margin_percent = (
        contribution_per_order
        / average_order_value
    )

else:

    contribution_margin_percent = 0

# ------------------------------------------------------------
# Monthly variable cost
# ------------------------------------------------------------

monthly_variable_cost = (
    monthly_orders
    * total_variable_cost_per_order
)

# ------------------------------------------------------------
# Total monthly operating cost
# ------------------------------------------------------------

total_monthly_operating_cost = (
    fixed_monthly_cost
    + monthly_variable_cost
)

# ------------------------------------------------------------
# Monthly operating profit
# ------------------------------------------------------------

monthly_profit = (
    monthly_revenue
    - total_monthly_operating_cost
)

# ------------------------------------------------------------
# Annual profit
# ------------------------------------------------------------

annual_profit = (
    monthly_profit * 12
)

# ------------------------------------------------------------
# ROI
# ------------------------------------------------------------

if initial_investment > 0:

    annual_roi = (
        annual_profit
        / initial_investment
    )

else:

    annual_roi = 0

# ------------------------------------------------------------
# Simple payback
# ------------------------------------------------------------

if monthly_profit > 0:

    simple_payback_months = (
        initial_investment
        / monthly_profit
    )

else:

    simple_payback_months = np.inf

# ============================================================
# BREAK-EVEN ANALYSIS
# ============================================================

if contribution_per_order > 0:

    break_even_orders_month = (
        fixed_monthly_cost
        / contribution_per_order
    )

    break_even_orders_day = (
        break_even_orders_month
        / operating_days
    )

    break_even_revenue_month = (
        break_even_orders_month
        * average_order_value
    )

else:

    break_even_orders_month = np.inf
    break_even_orders_day = np.inf
    break_even_revenue_month = np.inf

# ============================================================
# MAIN DASHBOARD
# ============================================================

st.header("📊 Business Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Monthly Revenue",
    f"£{monthly_revenue:,.0f}"
)

col2.metric(
    "Monthly Operating Cost",
    f"£{total_monthly_operating_cost:,.0f}"
)

col3.metric(
    "Monthly Profit",
    f"£{monthly_profit:,.0f}"
)

col4.metric(
    "Annual ROI",
    f"{annual_roi * 100:.1f}%"
)

# ============================================================
# KEY METRICS
# ============================================================

st.subheader("🎯 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Orders / Month",
    f"{monthly_orders:,.0f}"
)

col2.metric(
    "Contribution / Order",
    f"£{contribution_per_order:.2f}"
)

col3.metric(
    "Break-even Orders / Day",
    f"{break_even_orders_day:.1f}"
)

if np.isfinite(simple_payback_months):

    col4.metric(
        "Simple Payback",
        f"{simple_payback_months:.1f} months"
    )

else:

    col4.metric(
        "Simple Payback",
        "Not profitable"
    )

# ============================================================
# PROFITABILITY STATUS
# ============================================================

st.subheader("📌 Current Scenario")

if monthly_profit > 0:

    st.success(
        f"""
        **The business is currently profitable.**

        Monthly operating profit: **£{monthly_profit:,.0f}**

        Annual operating profit: **£{annual_profit:,.0f}**

        Annual ROI: **{annual_roi * 100:.1f}%**

        Simple payback period: **{simple_payback_months:.1f} months**
        """
    )

elif monthly_profit == 0:

    st.warning(
        "The business is exactly at operating break-even."
    )

else:

    st.error(
        f"""
        **The business is currently loss-making.**

        Monthly operating loss:
        **£{abs(monthly_profit):,.0f}**

        Break-even requirement:
        approximately **{break_even_orders_day:.1f} orders/day**
        """
    )

# ============================================================
# MONTHLY P&L
# ============================================================

st.header("📑 Monthly P&L")

pnl_data = pd.DataFrame({
    "Item": [
        "Revenue",
        "Food Cost",
        "Packaging",
        "Payment Fees",
        "Delivery Platform Fees",
        "Rent",
        "Employees",
        "Utilities",
        "Other Fixed Costs",
        "Operating Profit"
    ],
    "Monthly Amount (£)": [
        monthly_revenue,
        monthly_orders * food_cost_per_order,
        monthly_orders * packaging_cost_per_order,
        monthly_orders * payment_fee_per_order,
        monthly_orders * delivery_fee_per_order,
        rent,
        employee_cost,
        utilities,
        other_fixed_costs,
        monthly_profit
    ]
})

st.dataframe(
    pnl_data.style.format({
        "Monthly Amount (£)": "£{:,.0f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# COST BREAKDOWN
# ============================================================

st.header("💰 Monthly Cost Breakdown")

cost_data = pd.DataFrame({
    "Cost Category": [
        "Rent",
        "Employees",
        "Utilities",
        "Other Fixed Costs",
        "Food",
        "Packaging",
        "Payment Fees",
        "Delivery Platform"
    ],
    "Monthly Cost (£)": [
        rent,
        employee_cost,
        utilities,
        other_fixed_costs,
        monthly_orders * food_cost_per_order,
        monthly_orders * packaging_cost_per_order,
        monthly_orders * payment_fee_per_order,
        monthly_orders * delivery_fee_per_order
    ]
})

st.dataframe(
    cost_data.style.format({
        "Monthly Cost (£)": "£{:,.0f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# BREAK-EVEN ANALYSIS
# ============================================================

st.header("⚖️ Break-even Analysis")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Fixed Cost / Month",
    f"£{fixed_monthly_cost:,.0f}"
)

col2.metric(
    "Contribution / Order",
    f"£{contribution_per_order:.2f}"
)

col3.metric(
    "Break-even Orders / Day",
    f"{break_even_orders_day:.1f}"
)

st.info(
    f"""
    **Break-even calculation**

    Fixed monthly costs:
    £{fixed_monthly_cost:,.0f}

    Contribution per order:
    £{contribution_per_order:.2f}

    Required orders per month:
    {break_even_orders_month:,.0f}

    Required orders per day:
    **{break_even_orders_day:.1f}**

    Break-even monthly revenue:
    approximately **£{break_even_revenue_month:,.0f}**
    """
)

# ============================================================
# CUMULATIVE CASH FLOW / PAYBACK
# ============================================================

st.header("💰 Investment Payback")

st.write(
    """
    This chart shows how the initial investment is recovered over time.
    The business starts at negative initial investment and gradually
    recovers it through monthly operating profit.
    """
)

months = np.arange(0, analysis_months + 1)

# ------------------------------------------------------------
# Monthly values
# ------------------------------------------------------------

monthly_revenue_series = np.full(
    len(months),
    monthly_revenue
)

monthly_operating_cost_series = np.full(
    len(months),
    total_monthly_operating_cost
)

# Month 0 has no revenue / operating cost
monthly_revenue_series[0] = 0
monthly_operating_cost_series[0] = 0

# ------------------------------------------------------------
# Cumulative values
# ------------------------------------------------------------

cumulative_revenue = np.cumsum(
    monthly_revenue_series
)

cumulative_operating_cost = np.cumsum(
    monthly_operating_cost_series
)

# Initial investment is paid at Month 0
cumulative_total_cost = (
    initial_investment
    + cumulative_operating_cost
)

# Net cumulative cash flow
cumulative_cash_flow = (
    cumulative_revenue
    - cumulative_operating_cost
    - initial_investment
)

# ============================================================
# PAYBACK DETECTION
# ============================================================

payback_indices = np.where(
    cumulative_cash_flow >= 0
)[0]

if len(payback_indices) > 0:

    payback_month = int(
        payback_indices[0]
    )

else:

    payback_month = None

# ============================================================
# PAYBACK CHART — REVENUE VS COST
# ============================================================

cashflow_df = pd.DataFrame({
    "Month": months,
    "Cumulative Revenue (£)": cumulative_revenue,
    "Initial Investment + Operating Costs (£)": cumulative_total_cost
})

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    cashflow_df["Month"],
    cashflow_df["Cumulative Revenue (£)"],
    label="Cumulative Revenue",
    linewidth=2
)

ax.plot(
    cashflow_df["Month"],
    cashflow_df["Initial Investment + Operating Costs (£)"],
    label="Initial Investment + Operating Costs",
    linewidth=2
)

if payback_month is not None:

    payback_value = cumulative_revenue[
        payback_month
    ]

    ax.scatter(
        payback_month,
        payback_value,
        s=80,
        zorder=5
    )

    ax.annotate(
        f"Payback\nMonth {payback_month}",
        (
            payback_month,
            payback_value
        ),
        xytext=(10, 20),
        textcoords="offset points",
        fontsize=10
    )

ax.set_xlabel("Month")
ax.set_ylabel("Cumulative (£)")
ax.set_title(
    "Cumulative Revenue vs Investment + Operating Costs"
)

ax.grid(True, alpha=0.3)
ax.legend()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)

# ============================================================
# CUMULATIVE NET CASH FLOW
# ============================================================

st.subheader("📈 Cumulative Net Cash Flow")

cashflow_net_df = pd.DataFrame({
    "Month": months,
    "Net Cumulative Cash Flow (£)": cumulative_cash_flow
})

fig2, ax2 = plt.subplots(figsize=(12, 5))

ax2.plot(
    cashflow_net_df["Month"],
    cashflow_net_df["Net Cumulative Cash Flow (£)"],
    linewidth=2
)

ax2.axhline(
    y=0,
    linestyle="--",
    linewidth=1
)

if payback_month is not None:

    ax2.scatter(
        payback_month,
        cumulative_cash_flow[payback_month],
        s=80,
        zorder=5
    )

    ax2.annotate(
        f"Break-even: Month {payback_month}",
        (
            payback_month,
            0
        ),
        xytext=(10, 20),
        textcoords="offset points"
    )

ax2.set_xlabel("Month")
ax2.set_ylabel("Net Cumulative Cash Flow (£)")
ax2.set_title(
    "Investment Recovery Curve"
)

ax2.grid(True, alpha=0.3)

st.pyplot(
    fig2,
    use_container_width=True
)

plt.close(fig2)

# ============================================================
# PAYBACK SUMMARY
# ============================================================

st.subheader("📍 Payback Summary")

if payback_month is not None:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Initial Investment",
        f"£{initial_investment:,.0f}"
    )

    col2.metric(
        "Payback Month",
        f"Month {payback_month}"
    )

    col3.metric(
        "Monthly Operating Profit",
        f"£{monthly_profit:,.0f}"
    )

    st.success(
        f"""
        Based on the current assumptions, the initial
        **£{initial_investment:,.0f} investment is recovered
        around Month {payback_month}.**
        """
    )

else:

    st.warning(
        f"""
        Based on the current assumptions, the initial
        £{initial_investment:,.0f} investment is **not recovered
        within {analysis_months} months**.
        """
    )

# ============================================================
# CUSTOMER VOLUME SENSITIVITY
# ============================================================

st.header("📈 Customer Volume Sensitivity")

scenario_customers = range(20, 81, 5)

scenario_data = []

for customers in scenario_customers:

    orders = customers * operating_days

    revenue = (
        orders * average_order_value
    )

    variable_cost = (
        orders
        * total_variable_cost_per_order
    )

    profit = (
        revenue
        - variable_cost
        - fixed_monthly_cost
    )

    annual_profit_scenario = (
        profit * 12
    )

    roi_scenario = (
        annual_profit_scenario
        / initial_investment
        if initial_investment > 0
        else 0
    )

    if profit > 0:

        payback = (
            initial_investment / profit
        )

    else:

        payback = np.inf

    scenario_data.append({
        "Customers / Day": customers,
        "Monthly Revenue (£)": revenue,
        "Monthly Profit (£)": profit,
        "Annual ROI (%)": roi_scenario * 100,
        "Payback (Months)": payback
    })

scenario_df = pd.DataFrame(
    scenario_data
)

st.dataframe(
    scenario_df.style.format({
        "Monthly Revenue (£)": "£{:,.0f}",
        "Monthly Profit (£)": "£{:,.0f}",
        "Annual ROI (%)": "{:.1f}%",
        "Payback (Months)": "{:.1f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# PROFIT VS CUSTOMER VOLUME
# ============================================================

st.subheader("Monthly Profit vs Customer Volume")

profit_chart_df = scenario_df[
    [
        "Customers / Day",
        "Monthly Profit (£)"
    ]
].set_index(
    "Customers / Day"
)

st.line_chart(
    profit_chart_df
)

# ============================================================
# FINAL MODEL SUMMARY
# ============================================================

st.header("🧠 Model Summary")

summary_data = {
    "Initial Investment": f"£{initial_investment:,.0f}",
    "Customers / Day": f"{customers_per_day}",
    "Average Order Value": f"£{average_order_value:.2f}",
    "Food Cost / Order": f"£{food_cost_per_order:.2f}",
    "Contribution / Order": f"£{contribution_per_order:.2f}",
    "Monthly Revenue": f"£{monthly_revenue:,.0f}",
    "Monthly Operating Cost": f"£{total_monthly_operating_cost:,.0f}",
    "Monthly Operating Profit": f"£{monthly_profit:,.0f}",
    "Annual Operating Profit": f"£{annual_profit:,.0f}",
    "Annual ROI": f"{annual_roi * 100:.1f}%",
    "Break-even Orders / Day": f"{break_even_orders_day:.1f}",
    "Payback Period": (
        f"{payback_month} months"
        if payback_month is not None
        else "Not reached"
    )
}

summary_df = pd.DataFrame(
    summary_data.items(),
    columns=["Metric", "Value"]
)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "⚠️ This model is an estimate. Actual results will depend on "
    "sales volume, seasonality, staffing, taxes, platform commissions, "
    "food prices, wastage and other operating conditions."
)

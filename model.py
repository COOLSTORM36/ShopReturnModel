# Noodle Shop Business Model — Streamlit

```python
import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# Page config
# ============================================================

st.set_page_config(
    page_title="Noodle Shop Business Model",
    page_icon="🍜",
    layout="wide"
)

st.title("🍜 Noodle Shop Business Model")
st.caption("Small takeaway / delivery focused noodle shop")

# ============================================================
# Sidebar — Inputs
# ============================================================

st.sidebar.header("⚙️ Business Parameters")

# ------------------------------------------------------------
# Initial Investment
# ------------------------------------------------------------

st.sidebar.subheader("💷 Initial Investment")

initial_investment = st.sidebar.number_input(
    "Initial Investment (£)",
    min_value=0.0,
    value=50000.0,
    step=1000.0
)

# ------------------------------------------------------------
# Sales Parameters
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Variable Costs
# ------------------------------------------------------------

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
    step=1.0
)

# ------------------------------------------------------------
# Fixed Costs
# ------------------------------------------------------------

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
# Calculations
# ============================================================

# Employee cost
employee_cost = num_employees * salary_per_employee

# Fixed monthly costs
fixed_monthly_cost = (
    rent
    + employee_cost
    + utilities
    + other_fixed_costs
)

# Total orders per month
monthly_orders = customers_per_day * operating_days

# Revenue
monthly_revenue = monthly_orders * average_order_value

# Variable cost per order
payment_fee_per_order = (
    average_order_value * payment_fee_percent / 100
)

delivery_fee_per_order = (
    average_order_value * delivery_platform_percent / 100
)

total_variable_cost_per_order = (
    food_cost_per_order
    + packaging_cost_per_order
    + payment_fee_per_order
    + delivery_fee_per_order
)

# Contribution margin
contribution_per_order = (
    average_order_value
    - total_variable_cost_per_order
)

contribution_margin_percent = (
    contribution_per_order / average_order_value
    if average_order_value > 0
    else 0
)

# Monthly variable costs
monthly_variable_cost = (
    monthly_orders * total_variable_cost_per_order
)

# Monthly profit
monthly_profit = (
    monthly_revenue
    - monthly_variable_cost
    - fixed_monthly_cost
)

# Annual profit
annual_profit = monthly_profit * 12

# ROI
roi = (
    annual_profit / initial_investment
    if initial_investment > 0
    else 0
)

# Payback period
payback_months = (
    initial_investment / monthly_profit
    if monthly_profit > 0
    else np.inf
)

# ============================================================
# Break-even
# ============================================================

if contribution_per_order > 0:

    break_even_orders_month = (
        fixed_monthly_cost / contribution_per_order
    )

    break_even_orders_day = (
        break_even_orders_month / operating_days
    )

    break_even_revenue_month = (
        break_even_orders_month * average_order_value
    )

else:

    break_even_orders_month = np.inf
    break_even_orders_day = np.inf
    break_even_revenue_month = np.inf

# ============================================================
# Dashboard
# ============================================================

st.header("📊 Business Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Monthly Revenue",
    f"£{monthly_revenue:,.0f}"
)

col2.metric(
    "Monthly Costs",
    f"£{monthly_variable_cost + fixed_monthly_cost:,.0f}"
)

col3.metric(
    "Monthly Profit",
    f"£{monthly_profit:,.0f}"
)

col4.metric(
    "Annual ROI",
    f"{roi * 100:.1f}%"
)

# ============================================================
# Key Metrics
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

if np.isfinite(payback_months):
    col4.metric(
        "Payback Period",
        f"{payback_months:.1f} months"
    )
else:
    col4.metric(
        "Payback Period",
        "Not profitable"
    )

# ============================================================
# Cost Breakdown
# ============================================================

st.subheader("💰 Monthly Cost Breakdown")

cost_data = pd.DataFrame({
    "Cost": [
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
    cost_data,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# Profit & Loss
# ============================================================

st.subheader("📑 Monthly P&L")

pnl = pd.DataFrame({
    "Item": [
        "Revenue",
        "Variable Costs",
        "Fixed Costs",
        "Operating Profit"
    ],
    "Amount (£)": [
        monthly_revenue,
        monthly_variable_cost,
        fixed_monthly_cost,
        monthly_profit
    ]
})

st.dataframe(
    pnl,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# Scenario Analysis
# ============================================================

st.header("📈 Customer Volume Sensitivity")

scenario_customers = range(20, 81, 5)

scenario_data = []

for customers in scenario_customers:

    orders = customers * operating_days

    revenue = orders * average_order_value

    variable_cost = orders * total_variable_cost_per_order

    profit = (
        revenue
        - variable_cost
        - fixed_monthly_cost
    )

    annual_profit_scenario = profit * 12

    roi_scenario = (
        annual_profit_scenario / initial_investment
        if initial_investment > 0
        else 0
    )

    if profit > 0:
        payback = initial_investment / profit
    else:
        payback = np.inf

    scenario_data.append({
        "Customers / Day": customers,
        "Monthly Revenue (£)": revenue,
        "Monthly Profit (£)": profit,
        "Annual ROI (%)": roi_scenario * 100,
        "Payback (Months)": payback
    })

scenario_df = pd.DataFrame(scenario_data)

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
# Profit Chart
# ============================================================

st.subheader("Monthly Profit vs Customer Volume")

chart_df = scenario_df[
    ["Customers / Day", "Monthly Profit (£)"]
].set_index("Customers / Day")

st.line_chart(chart_df)

# ============================================================
# Business Interpretation
# ============================================================

st.header("🧠 Business Interpretation")

if monthly_profit > 0:

    st.success(
        f"""
        The business is currently profitable.

        Monthly operating profit:
        £{monthly_profit:,.0f}

        Annual operating profit:
        £{annual_profit:,.0f}

        Estimated annual ROI:
        {roi * 100:.1f}%

        Estimated payback period:
        {payback_months:.1f} months
        """
    )

else:

    st.error(
        f"""
        The business is currently loss-making.

        Monthly loss:
        £{abs(monthly_profit):,.0f}

        You need approximately
        {break_even_orders_day:.1f} customers/orders per day
        to reach break-even.
        """
    )

# ============================================================
# Break-even Summary
# ============================================================

st.header("⚖️ Break-even Analysis")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Fixed Costs / Month",
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
    Break-even formula:

    Fixed Monthly Costs ÷ Contribution per Order

    £{fixed_monthly_cost:,.0f} ÷ £{contribution_per_order:.2f}
    = {break_even_orders_month:,.0f} orders/month

    ≈ {break_even_orders_day:.1f} orders/day
    """
)
```

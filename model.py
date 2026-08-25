# ============================================================
# Cumulative Cash Flow / Payback Chart
# ============================================================

st.header("💰 Investment Payback Analysis")

analysis_months = st.slider(
    "Analysis Period (Months)",
    min_value=12,
    max_value=120,
    value=60,
    step=12
)

months = np.arange(0, analysis_months + 1)

# Monthly revenue and operating costs
monthly_revenue_constant = monthly_revenue
monthly_cost_constant = monthly_variable_cost + fixed_monthly_cost

# Cumulative revenue
cumulative_revenue = months * monthly_revenue_constant

# Cumulative operating costs
cumulative_operating_cost = months * monthly_cost_constant

# Total cash invested / required
# Initial investment is paid at Month 0
cumulative_total_investment = (
    initial_investment
    + cumulative_operating_cost
)

# Net cumulative cash generated after initial investment
cumulative_cash_flow = (
    cumulative_revenue
    - cumulative_operating_cost
    - initial_investment
)

# ------------------------------------------------------------
# Find payback month
# ------------------------------------------------------------

payback_index = np.where(cumulative_cash_flow >= 0)[0]

if len(payback_index) > 0:

    payback_month_chart = payback_index[0]

    st.success(
        f"🎉 Estimated payback point: "
        f"Month {payback_month_chart}"
    )

else:

    payback_month_chart = None

    st.warning(
        "The business does not recover the initial investment "
        "within the selected analysis period."
    )

# ------------------------------------------------------------
# Chart data
# ------------------------------------------------------------

cashflow_df = pd.DataFrame({
    "Month": months,
    "Cumulative Revenue (£)": cumulative_revenue,
    "Cumulative Operating Cost (£)": cumulative_operating_cost,
    "Initial Investment + Operating Costs (£)": cumulative_total_investment,
    "Net Cumulative Cash Flow (£)": cumulative_cash_flow
})

# ------------------------------------------------------------
# Display chart
# ------------------------------------------------------------

st.line_chart(
    cashflow_df.set_index("Month")[
        [
            "Cumulative Revenue (£)",
            "Initial Investment + Operating Costs (£)"
        ]
    ]
)

# ------------------------------------------------------------
# Payback details
# ------------------------------------------------------------

if payback_month_chart is not None:

    st.subheader("📍 Payback Point")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Initial Investment",
        f"£{initial_investment:,.0f}"
    )

    col2.metric(
        "Monthly Operating Profit",
        f"£{monthly_profit:,.0f}"
    )

    col3.metric(
        "Estimated Payback",
        f"{payback_month_chart} months"
    )

else:

    st.info(
        f"""
        At the current assumptions, the business does not
        recover the £{initial_investment:,.0f} initial investment
        within {analysis_months} months.
        """
    )

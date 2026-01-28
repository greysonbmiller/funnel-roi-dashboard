# -*- coding: utf-8 -*-
"""
Funnel Intelligence Bundle - Interactive ROI Dashboard
=======================================================
19,000-Unit Owner-Operator Business Case
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Funnel ROI Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .positive {
        color: #00C853;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    .highlight-box {
        background-color: #e8f4ea;
        border-left: 4px solid #00C853;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR - ASSUMPTION INPUTS
# =============================================================================
st.sidebar.markdown("## Model Assumptions")
st.sidebar.markdown("---")

# Portfolio Assumptions
st.sidebar.markdown("### Portfolio")
total_units = st.sidebar.number_input("Total Units", value=19000, min_value=1000, max_value=100000, step=1000)
avg_rent = st.sidebar.number_input("Average Monthly Rent ($)", value=1791, min_value=500, max_value=5000, step=50)
occupancy_rate = st.sidebar.slider("Occupancy Rate (%)", min_value=70, max_value=99, value=94) / 100
turnover_rate = st.sidebar.slider("Annual Turnover Rate (%)", min_value=30, max_value=70, value=50) / 100

st.sidebar.markdown("---")

# Cost Assumptions
st.sidebar.markdown("### Costs")
cost_per_turnover = st.sidebar.number_input("Cost per Turnover ($)", value=4000, min_value=1000, max_value=10000, step=250)
vacancy_days = st.sidebar.number_input("Vacancy Days per Turnover", value=30, min_value=14, max_value=60, step=1)
hourly_wage = st.sidebar.number_input("Leasing Staff Hourly Wage ($)", value=22, min_value=15, max_value=40, step=1)
marketing_cpl = st.sidebar.number_input("Marketing Cost per Lead ($)", value=35, min_value=10, max_value=100, step=5)

st.sidebar.markdown("---")

# Staffing Assumptions
st.sidebar.markdown("### Staffing")
units_per_staff = st.sidebar.slider(
    "Units per Leasing Staff Member",
    min_value=50,
    max_value=300,
    value=100,
    step=10,
    help="Industry standard: 100:1 (one staff per 100 units). Traditional ratio for total office staff including managers, leasing agents, etc."
)
st.sidebar.markdown(f"- Your ratio: {units_per_staff}:1 = ~{int(total_units/units_per_staff):,} staff")

st.sidebar.markdown("---")

# Funnel Assumptions
st.sidebar.markdown("### Funnel Performance")
funnel_price = st.sidebar.number_input("Funnel Price ($/unit/month)", value=3.70, min_value=1.00, max_value=12.00, step=0.10, format="%.2f")
conversion_lift = st.sidebar.slider("Conversion Improvement (%)", min_value=1.0, max_value=15.0, value=7.13, step=0.5) / 100
churn_reduction = st.sidebar.slider("Churn Reduction (%)", min_value=1.0, max_value=10.0, value=3.50, step=0.25) / 100
efficiency_improvement = st.sidebar.slider("Agent Efficiency Improvement (%)", min_value=10, max_value=35, value=20) / 100

st.sidebar.markdown("---")

# Scenario Selection
st.sidebar.markdown("### Scenario")
scenario = st.sidebar.radio("Select Scenario", ["Conservative (50%)", "Base Case (100%)", "Optimistic (150%)"])
scenario_multiplier = {"Conservative (50%)": 0.5, "Base Case (100%)": 1.0, "Optimistic (150%)": 1.5}[scenario]

# Staffing (user-adjustable ratio)
total_staff = int(total_units / units_per_staff)
monthly_leasing_hours = total_staff * 160  # Approximate monthly hours per FTE

# =============================================================================
# CALCULATIONS
# =============================================================================

# Portfolio Metrics
annual_revenue = total_units * avg_rent * occupancy_rate * 12
annual_leases = int(total_units * turnover_rate)
annual_lease_value = avg_rent * 12

# Value Driver 1: Conversion Improvement
additional_leases = annual_leases * conversion_lift * scenario_multiplier
conversion_benefit = additional_leases * annual_lease_value

# Value Driver 2: Churn Reduction
turnovers_avoided = annual_leases * churn_reduction * scenario_multiplier
turnover_savings = turnovers_avoided * cost_per_turnover
vacancy_savings = turnovers_avoided * vacancy_days * (avg_rent / 30)
retention_benefit = turnover_savings + vacancy_savings

# Value Driver 3: Labor Efficiency
annual_leasing_hours = monthly_leasing_hours * 12
hours_saved = annual_leasing_hours * efficiency_improvement * scenario_multiplier
labor_benefit = hours_saved * hourly_wage

# Value Driver 4: Marketing Efficiency
leads_per_lease = 33.7  # From analysis
marketing_value = additional_leases * leads_per_lease * marketing_cpl * 0.5 * scenario_multiplier
marketing_benefit = marketing_value

# Total Benefits
total_benefit = conversion_benefit + retention_benefit + labor_benefit + marketing_benefit

# Funnel Cost
monthly_cost = total_units * funnel_price
annual_cost = monthly_cost * 12

# ROI Metrics
net_benefit = total_benefit - annual_cost
roi_percentage = (net_benefit / annual_cost) * 100 if annual_cost > 0 else 0
payback_months = annual_cost / (total_benefit / 12) if total_benefit > 0 else 999
benefit_per_unit = total_benefit / total_units
cost_per_unit = annual_cost / total_units
net_per_unit = net_benefit / total_units

# =============================================================================
# MAIN CONTENT
# =============================================================================

# Header
st.markdown('<p class="main-header">Funnel Intelligence Bundle</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">ROI Business Case Analysis | 19,000-Unit Owner-Operator Portfolio</p>', unsafe_allow_html=True)
st.markdown("---")

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Annual Investment",
        value=f"${annual_cost:,.0f}",
        delta=f"${funnel_price:.2f}/unit/mo"
    )

with col2:
    st.metric(
        label="Total Annual Benefit",
        value=f"${total_benefit:,.0f}",
        delta=f"${benefit_per_unit:,.0f}/unit"
    )

with col3:
    st.metric(
        label="Net Annual Benefit",
        value=f"${net_benefit:,.0f}",
        delta=f"{roi_percentage:,.0f}% ROI",
        delta_color="normal"
    )

with col4:
    st.metric(
        label="Payback Period",
        value=f"{payback_months:.1f} months",
        delta="Quick payback" if payback_months < 3 else "Standard",
        delta_color="normal" if payback_months < 3 else "off"
    )

st.markdown("---")

# =============================================================================
# TABS
# =============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Summary",
    "Value Drivers",
    "Financial Model",
    "Sensitivity Analysis",
    "Stakeholder Views"
])

# =============================================================================
# TAB 1: EXECUTIVE SUMMARY
# =============================================================================
with tab1:
    st.markdown("## Executive Summary")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### The Opportunity")
        st.markdown(f"""
        Your **{total_units:,}-unit portfolio** generates **${annual_revenue/1e6:.1f}M** in annual revenue.
        With **{turnover_rate*100:.0f}% annual turnover**, you process approximately **{annual_leases:,} leases per year**.

        The Funnel Intelligence Bundle can transform your leasing operations through:
        - **AI-Powered Engagement** - 24/7 prospect response, 80% of inquiries handled automatically
        - **Improved Conversion** - {conversion_lift*100:.1f}% lift in lead-to-lease conversion
        - **Better Retention** - {churn_reduction*100:.1f}% reduction in resident churn
        - **Operational Efficiency** - {efficiency_improvement*100:.0f}% improvement in agent productivity
        """)

        st.markdown("### The Recommendation")

        if roi_percentage > 500:
            recommendation = "**STRONG BUY** - Exceptional ROI with rapid payback"
            color = "green"
        elif roi_percentage > 100:
            recommendation = "**BUY** - Solid ROI justifies investment"
            color = "green"
        elif roi_percentage > 0:
            recommendation = "**CONSIDER** - Positive ROI, evaluate strategic fit"
            color = "orange"
        else:
            recommendation = "**REVIEW** - Adjust assumptions or scope"
            color = "red"

        st.markdown(f"""
        <div class="highlight-box">
            <strong style="font-size: 1.2em;">{recommendation}</strong><br><br>
            At <strong>${funnel_price:.2f}/unit/month</strong>, Funnel generates <strong>${net_per_unit:,.0f}</strong>
            in annual net benefit per unit. The investment pays for itself in <strong>{payback_months:.1f} months</strong>.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Donut chart for value distribution
        fig = go.Figure(data=[go.Pie(
            labels=['Conversion', 'Retention', 'Labor', 'Marketing'],
            values=[conversion_benefit, retention_benefit, labor_benefit, marketing_benefit],
            hole=.6,
            marker_colors=['#667eea', '#764ba2', '#f093fb', '#f5576c']
        )])
        fig.update_layout(
            title="Annual Benefit Distribution",
            showlegend=True,
            height=350,
            margin=dict(t=50, b=0, l=0, r=0)
        )
        fig.add_annotation(
            text=f"${total_benefit/1e6:.1f}M/yr",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 2: VALUE DRIVERS
# =============================================================================
with tab2:
    st.markdown("## Value Driver Analysis")

    # Value drivers table
    value_data = {
        'Value Driver': ['Conversion Improvement', 'Churn Reduction', 'Labor Efficiency', 'Marketing Efficiency'],
        'Annual Benefit': [conversion_benefit, retention_benefit, labor_benefit, marketing_benefit],
        '% of Total': [
            conversion_benefit/total_benefit*100 if total_benefit > 0 else 0,
            retention_benefit/total_benefit*100 if total_benefit > 0 else 0,
            labor_benefit/total_benefit*100 if total_benefit > 0 else 0,
            marketing_benefit/total_benefit*100 if total_benefit > 0 else 0
        ],
        'Key Funnel Feature': [
            'Prospect AI, CRM, AI Chatbot',
            'Resident AI, Renewal Automation',
            'Centralized CRM, AI Workflows',
            'Multi-touch Attribution'
        ]
    }

    col1, col2 = st.columns([1, 1])

    with col1:
        # Bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=['Conversion', 'Retention', 'Labor', 'Marketing'],
                y=[conversion_benefit, retention_benefit, labor_benefit, marketing_benefit],
                marker_color=['#667eea', '#764ba2', '#f093fb', '#f5576c'],
                text=[f'${v/1e6:.2f}M' for v in [conversion_benefit, retention_benefit, labor_benefit, marketing_benefit]],
                textposition='outside'
            )
        ])
        fig.update_layout(
            title="Annual Benefit by Value Driver",
            yaxis_title="Annual Benefit ($)",
            height=500,
            showlegend=False,
            margin=dict(t=80, b=60, l=60, r=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Value Driver Details (Annual)")

        st.markdown(f"""
        **Conversion Improvement: ${conversion_benefit:,.0f}/year**
        - Additional leases: {additional_leases:,.0f}
        - Value per lease: ${annual_lease_value:,.0f}
        - Driven by: 24/7 AI engagement, faster response

        **Churn Reduction: ${retention_benefit:,.0f}/year**
        - Turnovers avoided: {turnovers_avoided:,.0f}
        - Turnover cost savings: ${turnover_savings:,.0f}
        - Vacancy savings: ${vacancy_savings:,.0f}

        **Labor Efficiency: ${labor_benefit:,.0f}/year**
        - Hours saved: {hours_saved:,.0f}
        - At ${hourly_wage}/hour
        - Enables centralization strategy

        **Marketing Efficiency: ${marketing_benefit:,.0f}/year**
        - Better conversion = lower cost per lease
        - Multi-touch attribution
        """)

    st.markdown("---")

    # Detailed breakdown
    st.markdown("### Funnel Features Mapped to Value")

    features_col1, features_col2 = st.columns(2)

    with features_col1:
        st.markdown("""
        **AI Suite (Drives Conversion + Labor)**
        - Prospect AI - SMS/email virtual assistant
        - AI Chatbot - Website engagement
        - Voice AI - Phone interactions
        - AI Call Summaries - Documentation
        - AI Message Suggestions - Response quality
        - AI Tour Scheduling - Automation
        """)

    with features_col2:
        st.markdown("""
        **Platform Features (Drives Retention + Efficiency)**
        - Resident AI - Renewal automation
        - Centralized CRM - Portfolio-wide view
        - Online Leasing - 70% faster approvals
        - Resident Portal - Self-service
        - Multi-touch Attribution - Marketing ROI
        - Cross-selling - 800 bps improvement
        """)

# =============================================================================
# TAB 3: FINANCIAL MODEL
# =============================================================================
with tab3:
    st.markdown("## Financial Model")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Investment")

        investment_data = pd.DataFrame({
            'Item': ['Per Unit (Monthly)', 'Per Unit (Annual)', 'Portfolio (Monthly)', 'Portfolio (Annual)'],
            'Amount': [f'${funnel_price:.2f}', f'${funnel_price*12:.2f}', f'${monthly_cost:,.0f}', f'${annual_cost:,.0f}']
        })
        st.table(investment_data)

        st.markdown("### What's Included")
        st.markdown("""
        - CRM with omni-channel communications
        - Full AI Suite (Prospect AI, Resident AI, Voice AI)
        - Online Leasing with FinTech verification
        - Resident Portal
        - PMS integration & maintenance
        - Reporting & analytics
        """)

    with col2:
        st.markdown("### Returns")

        returns_data = pd.DataFrame({
            'Metric': ['Total Annual Benefit', 'Total Annual Cost', 'Net Annual Benefit', 'ROI', 'Payback Period'],
            'Value': [
                f'${total_benefit:,.0f}',
                f'${annual_cost:,.0f}',
                f'${net_benefit:,.0f}',
                f'{roi_percentage:,.0f}%',
                f'{payback_months:.1f} months'
            ]
        })
        st.table(returns_data)

        st.markdown("### Per-Unit Economics")
        per_unit_data = pd.DataFrame({
            'Metric': ['Annual Benefit', 'Annual Cost', 'Net Benefit'],
            'Per Unit': [f'${benefit_per_unit:,.2f}', f'${cost_per_unit:,.2f}', f'${net_per_unit:,.2f}']
        })
        st.table(per_unit_data)

    st.markdown("---")

    # 5-Year Projection
    st.markdown("### 5-Year Value Projection")

    years = [0, 1, 2, 3, 4, 5]
    cumulative_benefit = [total_benefit * y for y in years]
    cumulative_cost = [annual_cost * y for y in years]
    cumulative_net = [b - c for b, c in zip(cumulative_benefit, cumulative_cost)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=cumulative_benefit, name='Cumulative Benefit', line=dict(color='#00C853', width=3)))
    fig.add_trace(go.Scatter(x=years, y=cumulative_cost, name='Cumulative Cost', line=dict(color='#f5576c', width=3)))
    fig.add_trace(go.Scatter(x=years, y=cumulative_net, name='Cumulative Net', line=dict(color='#667eea', width=3), fill='tozeroy'))

    fig.update_layout(
        title="5-Year Financial Projection",
        xaxis_title="Year",
        yaxis_title="Cumulative Value ($)",
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="highlight-box">
        <strong>5-Year Total Value:</strong><br>
        Total Benefit: <strong>${cumulative_benefit[-1]:,.0f}</strong> |
        Total Cost: <strong>${cumulative_cost[-1]:,.0f}</strong> |
        Net Value: <strong>${cumulative_net[-1]:,.0f}</strong>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# TAB 4: SENSITIVITY ANALYSIS
# =============================================================================
with tab4:
    st.markdown("## Sensitivity Analysis")

    st.markdown("### Scenario Comparison")

    # Calculate scenarios (independent of sidebar scenario selection)
    scenarios_data = []
    for mult, name in [(0.5, 'Conservative'), (1.0, 'Base Case'), (1.5, 'Optimistic')]:
        # Recalculate using base values (without sidebar scenario_multiplier)
        s_additional_leases = annual_leases * conversion_lift * mult
        s_conv = s_additional_leases * annual_lease_value
        s_ret = (annual_leases * churn_reduction * mult * cost_per_turnover) + (annual_leases * churn_reduction * mult * vacancy_days * avg_rent / 30)
        s_lab = annual_leasing_hours * efficiency_improvement * mult * hourly_wage
        s_mkt = s_additional_leases * leads_per_lease * marketing_cpl * 0.5
        s_total = s_conv + s_ret + s_lab + s_mkt
        s_net = s_total - annual_cost
        s_roi = (s_net / annual_cost) * 100
        s_payback = annual_cost / (s_total / 12) if s_total > 0 else 999

        scenarios_data.append({
            'Scenario': name,
            'Total Benefit': s_total,
            'Net Benefit': s_net,
            'ROI (%)': s_roi,
            'Payback (mo)': s_payback
        })

    scenarios_df = pd.DataFrame(scenarios_data)

    col1, col2 = st.columns(2)

    with col1:
        # Scenario comparison bar chart
        fig = go.Figure(data=[
            go.Bar(name='Total Benefit', x=scenarios_df['Scenario'], y=scenarios_df['Total Benefit'], marker_color='#667eea'),
            go.Bar(name='Net Benefit', x=scenarios_df['Scenario'], y=scenarios_df['Net Benefit'], marker_color='#00C853')
        ])
        fig.update_layout(
            title="Benefit by Scenario",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Scenario Results")
        display_df = scenarios_df.copy()
        display_df['Total Benefit'] = display_df['Total Benefit'].apply(lambda x: f'${x:,.0f}')
        display_df['Net Benefit'] = display_df['Net Benefit'].apply(lambda x: f'${x:,.0f}')
        display_df['ROI (%)'] = display_df['ROI (%)'].apply(lambda x: f'{x:,.0f}%')
        display_df['Payback (mo)'] = display_df['Payback (mo)'].apply(lambda x: f'{x:.1f}')
        st.table(display_df)

        st.markdown("""
        <div class="warning-box">
            <strong>Key Insight:</strong> Even in the conservative scenario (50% of projected benefits),
            the investment remains highly profitable with strong ROI and quick payback.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Single variable sensitivity (uses base case, not sidebar scenario)
    st.markdown("### Single Variable Sensitivity (Base Case)")

    # Calculate base benefits without scenario multiplier for sensitivity analysis
    base_conversion_benefit = annual_leases * conversion_lift * annual_lease_value
    base_retention_benefit = (annual_leases * churn_reduction * cost_per_turnover) + (annual_leases * churn_reduction * vacancy_days * avg_rent / 30)
    base_labor_benefit = annual_leasing_hours * efficiency_improvement * hourly_wage
    base_additional_leases = annual_leases * conversion_lift
    base_marketing_benefit = base_additional_leases * leads_per_lease * marketing_cpl * 0.5

    sensitivity_var = st.selectbox(
        "Select variable to analyze:",
        ["Conversion Improvement", "Churn Reduction", "Efficiency Improvement", "Funnel Price"]
    )

    if sensitivity_var == "Conversion Improvement":
        var_range = [x/100 for x in range(1, 16)]
        var_label = "Conversion Improvement (%)"
        results = []
        for v in var_range:
            s_conv = annual_leases * v * annual_lease_value
            s_total = s_conv + base_retention_benefit + base_labor_benefit + base_marketing_benefit
            results.append({'Variable': v*100, 'Net Benefit': s_total - annual_cost})

    elif sensitivity_var == "Churn Reduction":
        var_range = [x/100 for x in range(1, 11)]
        var_label = "Churn Reduction (%)"
        results = []
        for v in var_range:
            s_ret = (annual_leases * v * cost_per_turnover) + (annual_leases * v * vacancy_days * avg_rent / 30)
            s_total = base_conversion_benefit + s_ret + base_labor_benefit + base_marketing_benefit
            results.append({'Variable': v*100, 'Net Benefit': s_total - annual_cost})

    elif sensitivity_var == "Efficiency Improvement":
        var_range = [x/100 for x in range(10, 36, 5)]
        var_label = "Efficiency Improvement (%)"
        results = []
        for v in var_range:
            s_lab = annual_leasing_hours * v * hourly_wage
            s_total = base_conversion_benefit + base_retention_benefit + s_lab + base_marketing_benefit
            results.append({'Variable': v*100, 'Net Benefit': s_total - annual_cost})

    else:  # Funnel Price
        var_range = [x/10 for x in range(20, 60, 5)]
        var_label = "Funnel Price ($/unit/month)"
        results = []
        for v in var_range:
            s_cost = total_units * v * 12
            s_total = base_conversion_benefit + base_retention_benefit + base_labor_benefit + base_marketing_benefit
            results.append({'Variable': v, 'Net Benefit': s_total - s_cost})

    results_df = pd.DataFrame(results)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=results_df['Variable'],
        y=results_df['Net Benefit'],
        mode='lines+markers',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title=f"Net Benefit Sensitivity to {sensitivity_var}",
        xaxis_title=var_label,
        yaxis_title="Net Annual Benefit ($)",
        height=400
    )
    # Add reference line at base case value
    base_net_benefit = base_conversion_benefit + base_retention_benefit + base_labor_benefit + base_marketing_benefit - annual_cost
    fig.add_hline(y=base_net_benefit, line_dash="dash", line_color="green",
                  annotation_text=f"Base Case: ${base_net_benefit:,.0f}")
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 5: STAKEHOLDER VIEWS
# =============================================================================
with tab5:
    st.markdown("## Stakeholder Perspectives")

    stakeholder = st.radio(
        "Select Stakeholder View:",
        ["CFO", "VP of Marketing", "SVP of Operations"],
        horizontal=True
    )

    if stakeholder == "CFO":
        st.markdown("### CFO View: Financial Performance")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Investment", f"${annual_cost:,.0f}/yr", f"${cost_per_unit:.2f}/unit")
        with col2:
            st.metric("Net Benefit", f"${net_benefit:,.0f}", f"{roi_percentage:,.0f}% ROI")
        with col3:
            st.metric("Payback", f"{payback_months:.1f} months", "Quick" if payback_months < 3 else "Standard")

        st.markdown(f"""
        ### Key Financial Metrics

        | Metric | Value |
        |--------|-------|
        | Annual Investment | ${annual_cost:,.0f} |
        | Annual Benefit | ${total_benefit:,.0f} |
        | Net Benefit | ${net_benefit:,.0f} |
        | ROI | {roi_percentage:,.0f}% |
        | Payback Period | {payback_months:.1f} months |
        | 5-Year Net Value | ${net_benefit * 5:,.0f} |

        ### Per-Unit Economics

        | Metric | Monthly | Annual |
        |--------|---------|--------|
        | Cost | ${funnel_price:.2f} | ${funnel_price*12:.2f} |
        | Benefit | ${benefit_per_unit/12:.2f} | ${benefit_per_unit:.2f} |
        | Net | ${net_per_unit/12:.2f} | ${net_per_unit:.2f} |

        ### CFO Talking Points
        - Investment pays for itself in {payback_months:.1f} months
        - {roi_percentage:,.0f}% ROI exceeds typical technology investment thresholds
        - Operating expense (not CapEx) - ${funnel_price:.2f}/unit/month
        - Scales with portfolio - costs aligned with revenue
        """)

    elif stakeholder == "VP of Marketing":
        st.markdown("### VP of Marketing View: Lead Performance")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Additional Leases", f"{additional_leases:,.0f}/yr", f"+{conversion_lift*100:.1f}% conversion")
        with col2:
            st.metric("Marketing Efficiency", f"${marketing_benefit:,.0f}", "Better attribution")
        with col3:
            st.metric("Lead Response", "24/7", "AI-powered")

        st.markdown(f"""
        ### Marketing Impact

        | Metric | Current | With Funnel | Improvement |
        |--------|---------|-------------|-------------|
        | Lead Response Time | Variable | <5 minutes | Instant 24/7 |
        | Lead-to-Lease Conversion | Baseline | +{conversion_lift*100:.1f}% | {additional_leases:,.0f} more leases |
        | Inquiry Handling | Manual | 80% automated | AI-powered |
        | Attribution | Limited | Multi-touch | Full visibility |

        ### Features for Marketing
        - **Prospect AI** - Handles 80% of initial inquiries automatically
        - **AI Chatbot** - Website engagement, lead capture
        - **Multi-touch Attribution** - Know which channels drive leases
        - **Cross-selling** - 800 bps improvement in referrals
        - **ILS Syndication** - Optimized listings across platforms

        ### Marketing ROI
        - Additional {additional_leases:,.0f} leases = ${conversion_benefit:,.0f} revenue
        - Same lead volume, better conversion
        - Full visibility into marketing spend effectiveness
        """)

    else:  # SVP of Operations
        st.markdown("### SVP of Operations View: Efficiency & Centralization")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Hours Saved", f"{hours_saved:,.0f}/yr", f"{efficiency_improvement*100:.0f}% efficiency")
        with col2:
            st.metric("Turnovers Avoided", f"{turnovers_avoided:,.0f}", f"${retention_benefit:,.0f} saved")
        with col3:
            new_ratio = total_units / (total_staff * (1 - efficiency_improvement))
            st.metric("Agent Ratio", f"{units_per_staff}:1 → {new_ratio:.0f}:1", "Centralization enabled")

        st.markdown(f"""
        ### Operational Impact

        | Metric | Current | With Funnel | Improvement |
        |--------|---------|-------------|-------------|
        | Annual Leasing Hours | {annual_leasing_hours:,.0f} | {annual_leasing_hours - hours_saved:,.0f} | -{hours_saved:,.0f} hours |
        | Agent-to-Unit Ratio | {units_per_staff}:1 | {new_ratio:.0f}:1 | +{efficiency_improvement*100:.0f}% efficiency |
        | Annual Turnovers | {annual_leases:,} | {annual_leases - turnovers_avoided:,.0f} | -{turnovers_avoided:,.0f} |
        | Labor Cost Savings | - | ${labor_benefit:,.0f} | Redeployable |

        ### Centralization Enablement

        The {efficiency_improvement*100:.0f}% efficiency improvement enables:
        - **Same staff, more units** - Handle growth without adding headcount
        - **Centralized model** - Move from on-site to hub model
        - **Higher-value work** - Staff focuses on tours and closings, not data entry

        ### Features for Operations
        - **Centralized CRM** - Portfolio-wide visibility
        - **AI Workflows** - Automated follow-ups and tasks
        - **AI Call Summaries** - Instant documentation
        - **AI Suggestions** - Guided responses
        - **35% task time reduction** - Documented efficiency gain

        ### Retention Impact
        - {turnovers_avoided:,.0f} fewer turnover events
        - ${turnover_savings:,.0f} in direct cost savings
        - ${vacancy_savings:,.0f} in avoided vacancy loss
        """)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p><strong>Funnel Intelligence Bundle - ROI Analysis Dashboard</strong></p>
    <p>Interactive model for 19,000-unit owner-operator portfolio evaluation</p>
    <p>Adjust assumptions in the sidebar to see real-time impact on ROI</p>
</div>
""", unsafe_allow_html=True)

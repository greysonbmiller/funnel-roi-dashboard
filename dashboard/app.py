# -*- coding: utf-8 -*-
"""
Funnel Intelligence Bundle - Interactive ROI Dashboard
=======================================================
19,000-Unit Owner-Operator Business Case
Data-Driven Analysis with Conservative Methodology
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Funnel ROI Analysis",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling - Funnel brand colors
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #E91E8C 0%, #FF9B7F 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #E91E8C 0%, #FF9B7F 100%);
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
        color: #E91E8C;
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
        background: linear-gradient(135deg, #E91E8C 0%, #FF9B7F 100%);
        color: white;
    }
    .highlight-box {
        background-color: #FFE8F5;
        border-left: 4px solid #E91E8C;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #FFF5F0;
        border-left: 4px solid #FF9B7F;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .data-quality-box {
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .soft-benefit-box {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    [data-testid="stSidebar"] h2 {
        color: #E91E8C;
        font-weight: 600;
    }
    [data-testid="stSidebar"] h3 {
        color: #2D2D2D;
        font-weight: 600;
        margin-top: 1rem;
    }
    [data-testid="stSidebar"] {
        background-color: #FAFAFA;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# LOAD ACTUAL DATA FROM EXCEL
# =============================================================================
@st.cache_data
def load_data():
    """Load and process data from Excel file."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    # Try multiple potential paths (for local dev and Streamlit Cloud)
    possible_paths = [
        # Relative to repo root (most likely for Streamlit Cloud)
        os.path.join(repo_root, 'Value Engineer _ Case Study Data.xlsx'),
        # Current working directory
        'Value Engineer _ Case Study Data.xlsx',
        # Relative to dashboard folder going up one level
        os.path.join(script_dir, '..', 'Value Engineer _ Case Study Data.xlsx'),
        # Absolute path for local development
        r'C:\Users\Lenovo\Documents\Work\Funnel Leasing\Value Engineer _ Case Study Data.xlsx',
    ]

    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break

    if file_path is None:
        # Debug: show what paths were tried and current working directory
        return None, f"Data file not found. CWD: {os.getcwd()}, Script dir: {script_dir}, Tried: {possible_paths}"

    try:
        # Load all sheets
        properties_df = pd.read_excel(file_path, sheet_name='properties')
        performance_df = pd.read_excel(file_path, sheet_name='performance')
        staffing_df = pd.read_excel(file_path, sheet_name='staffing')
        assumptions_df = pd.read_excel(file_path, sheet_name='Funnel assumptions')

        # Merge all data
        df = properties_df.merge(performance_df, on='property_id')
        df = df.merge(staffing_df, on='property_id')
        df = df.merge(assumptions_df, on='property_id')

        # Track missing values before filling
        missing_info = {
            'contact_rate': df['contact_rate'].isnull().sum(),
            'avg_rent': df['avg_rent'].isnull().sum(),
            'leasing_staff_hours': df['leasing_staff_hours'].isnull().sum()
        }

        # Fill missing values with median
        df['contact_rate'] = df['contact_rate'].fillna(df['contact_rate'].median())
        df['avg_rent'] = df['avg_rent'].fillna(df['avg_rent'].median())
        df['leasing_staff_hours'] = df['leasing_staff_hours'].fillna(df['leasing_staff_hours'].median())

        # Calculate portfolio-level metrics from actual data
        data_summary = {
            'total_properties': len(df),
            # Units statistics
            'total_units': df['units'].sum(),
            'units_mean': df['units'].mean(),
            'units_median': df['units'].median(),
            'units_std': df['units'].std(),
            'units_min': df['units'].min(),
            'units_max': df['units'].max(),
            # Rent statistics
            'avg_rent': df['avg_rent'].mean(),
            'avg_rent_median': df['avg_rent'].median(),
            'avg_rent_std': df['avg_rent'].std(),
            'avg_rent_min': df['avg_rent'].min(),
            'avg_rent_max': df['avg_rent'].max(),
            # Leads and performance
            'total_monthly_leads': df['monthly_leads'].sum(),
            'avg_contact_rate': df['contact_rate'].mean(),
            'total_monthly_tours': df['tours_booked'].sum(),
            # Staffing statistics
            'total_onsite_staff': df['onsite_staff_count'].sum(),
            'staff_mean': df['onsite_staff_count'].mean(),
            'staff_median': df['onsite_staff_count'].median(),
            'staff_std': df['onsite_staff_count'].std(),
            'total_monthly_leasing_hours': df['leasing_staff_hours'].sum(),
            # Conversion lift statistics
            'avg_conversion_lift': df['funnel_lead_to_lease_improvement_pct'].mean(),
            'conversion_lift_median': df['funnel_lead_to_lease_improvement_pct'].median(),
            'conversion_lift_std': df['funnel_lead_to_lease_improvement_pct'].std(),
            'conversion_lift_min': df['funnel_lead_to_lease_improvement_pct'].min(),
            'conversion_lift_max': df['funnel_lead_to_lease_improvement_pct'].max(),
            # Churn reduction statistics
            'avg_churn_reduction': df['funnel_churn_reduction_pct'].mean(),
            'churn_reduction_median': df['funnel_churn_reduction_pct'].median(),
            'churn_reduction_std': df['funnel_churn_reduction_pct'].std(),
            'churn_reduction_min': df['funnel_churn_reduction_pct'].min(),
            'churn_reduction_max': df['funnel_churn_reduction_pct'].max(),
            # Efficiency improvement statistics
            'avg_efficiency_improvement': df['funnel_agent_to_unit_ratio_improvement_pct'].mean(),
            'efficiency_std': df['funnel_agent_to_unit_ratio_improvement_pct'].std(),
            # Missing data info
            'missing_info': missing_info
        }

        return df, data_summary
    except Exception as e:
        return None, str(e)

# Load data
df, data_result = load_data()

if df is None:
    st.error(f"Error loading data: {data_result}")
    st.stop()

data_summary = data_result

# =============================================================================
# SIDEBAR - ASSUMPTION INPUTS (with data-driven defaults)
# =============================================================================
st.sidebar.markdown("## Model Assumptions")
st.sidebar.markdown("*Defaults loaded from actual data*")
st.sidebar.markdown("---")

# Portfolio Assumptions (from data)
st.sidebar.markdown("### Portfolio")
total_units = st.sidebar.number_input(
    "Total Units",
    value=int(data_summary['total_units']),
    min_value=1000,
    max_value=100000,
    step=1000,
    help=f"**From Data:** Sum of {data_summary['total_properties']:,} properties\n\n"
         f"- Mean per property: {data_summary['units_mean']:.1f} units\n"
         f"- Median: {data_summary['units_median']:.0f} units\n"
         f"- Std Dev: {data_summary['units_std']:.1f}\n"
         f"- Range: {data_summary['units_min']:,} - {data_summary['units_max']:,} units"
)
avg_rent = st.sidebar.number_input(
    "Average Monthly Rent ($)",
    value=int(round(data_summary['avg_rent'])),
    min_value=500,
    max_value=5000,
    step=50,
    help=f"**From Data:** Portfolio average rent\n\n"
         f"- Mean: ${data_summary['avg_rent']:,.0f}\n"
         f"- Median: ${data_summary['avg_rent_median']:,.0f}\n"
         f"- Std Dev: ${data_summary['avg_rent_std']:,.0f}\n"
         f"- Range: ${data_summary['avg_rent_min']:,.0f} - ${data_summary['avg_rent_max']:,.0f}\n"
         f"- Missing values: {data_summary['missing_info']['avg_rent']} (filled with median)"
)
occupancy_rate = st.sidebar.slider(
    "Occupancy Rate (%)",
    min_value=70,
    max_value=99,
    value=94,
    help="**Industry Assumption:** Not in dataset\n\n"
         "- 94% is typical for stabilized multifamily\n"
         "- Class A: 93-96%\n"
         "- Class B: 91-95%\n"
         "- Class C: 88-93%"
) / 100
turnover_rate = st.sidebar.slider(
    "Annual Turnover Rate (%)",
    min_value=30,
    max_value=70,
    value=50,
    help="**Industry Assumption:** Not in dataset\n\n"
         "- 50% is national average\n"
         "- Class A (Luxury): 40-50%\n"
         "- Class B: 50-55%\n"
         "- Class C: 55-65%\n"
         "- Student Housing: 90-100%"
) / 100

st.sidebar.markdown("---")

# Cost Assumptions
st.sidebar.markdown("### Costs")
cost_per_turnover = st.sidebar.number_input(
    "Cost per Turnover ($)",
    value=4000,
    min_value=1000,
    max_value=10000,
    step=250,
    help="**Industry Assumption:** Not in dataset\n\n"
         "Includes: cleaning, repairs, marketing, admin time\n\n"
         "- Budget properties: $2,500-$3,500\n"
         "- Mid-range: $3,500-$4,500\n"
         "- Class A/Luxury: $4,500-$6,000+\n"
         "- NAA benchmark: ~$4,000"
)
vacancy_days = st.sidebar.number_input(
    "Vacancy Days per Turnover",
    value=30,
    min_value=14,
    max_value=60,
    step=1,
    help="**Industry Assumption:** Not in dataset\n\n"
         "Days unit sits empty during turnover\n\n"
         "- High demand markets: 14-21 days\n"
         "- Average markets: 25-35 days\n"
         "- Slower markets: 35-60 days\n"
         "- Industry average: ~30 days"
)
vacancy_days_saved = st.sidebar.number_input(
    "Vacancy Days Saved per Additional Lease",
    value=10,
    min_value=5,
    max_value=30,
    step=1,
    help="**Conservative Estimate**\n\n"
         "How many days faster units lease with Funnel\n\n"
         "- Conservative: 5-10 days\n"
         "- Moderate: 10-15 days\n"
         "- Aggressive: 15-30 days\n\n"
         "This is the key driver of conversion benefit"
)
hourly_wage = st.sidebar.number_input(
    "Leasing Staff Hourly Wage ($)",
    value=22,
    min_value=15,
    max_value=40,
    step=1,
    help="**Industry Assumption:** Not in dataset\n\n"
         "Fully-loaded hourly cost for leasing staff\n\n"
         "- Entry level: $15-$18/hr\n"
         "- Experienced: $18-$25/hr\n"
         "- Senior/Urban: $25-$35/hr\n"
         "- With benefits (~30%): add $5-$8/hr"
)

st.sidebar.markdown("---")

# Staffing Assumptions (from actual data)
st.sidebar.markdown("### Staffing")
actual_units_per_staff = data_summary['total_units'] / data_summary['total_onsite_staff']
units_per_staff = st.sidebar.slider(
    "Units per Leasing Staff Member",
    min_value=10,
    max_value=50,
    value=round(actual_units_per_staff),
    step=1,
    help=f"**From Data:** Calculated from staffing sheet\n\n"
         f"- Portfolio ratio: **{actual_units_per_staff:.1f}:1**\n"
         f"- Total staff: {int(data_summary['total_onsite_staff']):,}\n"
         f"- Total units: {int(data_summary['total_units']):,}\n\n"
         f"**Per Property Stats:**\n"
         f"- Mean staff: {data_summary['staff_mean']:.1f}\n"
         f"- Median staff: {data_summary['staff_median']:.0f}\n"
         f"- Std Dev: {data_summary['staff_std']:.1f}\n\n"
         f"Industry typical: 50-100 units per agent"
)
st.sidebar.markdown(f"- Data shows: **{actual_units_per_staff:.1f}:1** ratio")
st.sidebar.markdown(f"- Total staff from data: {int(data_summary['total_onsite_staff']):,}")

st.sidebar.markdown("---")

# Funnel Assumptions (from data)
st.sidebar.markdown("### Funnel Performance")
st.sidebar.markdown("*From dataset assumptions*")
funnel_price = st.sidebar.number_input(
    "Funnel Price ($/unit/month)",
    value=3.70,
    min_value=1.00,
    max_value=12.00,
    step=0.10,
    format="%.2f",
    help="**Pricing Assumption**\n\n"
         "Funnel Intelligence Bundle pricing\n\n"
         "- Entry tier: $3.7/unit/mo"
)
conversion_lift = st.sidebar.slider(
    "Conversion Improvement (%)",
    min_value=1.0,
    max_value=15.0,
    value=round(data_summary['avg_conversion_lift'] * 100, 1),
    step=0.5,
    help=f"**From Data:** Funnel assumptions sheet\n\n"
         f"- Mean: **{data_summary['avg_conversion_lift']*100:.2f}%**\n"
         f"- Median: {data_summary['conversion_lift_median']*100:.2f}%\n"
         f"- Std Dev: {data_summary['conversion_lift_std']*100:.2f}%\n"
         f"- Range: {data_summary['conversion_lift_min']*100:.1f}% - {data_summary['conversion_lift_max']*100:.1f}%\n\n"
         f"Improvement in lead-to-lease conversion rate"
) / 100
churn_reduction = st.sidebar.slider(
    "Churn Reduction (%)",
    min_value=1.0,
    max_value=10.0,
    value=round(data_summary['avg_churn_reduction'] * 100, 2),
    step=0.25,
    help=f"**From Data:** Funnel assumptions sheet\n\n"
         f"- Mean: **{data_summary['avg_churn_reduction']*100:.2f}%**\n"
         f"- Median: {data_summary['churn_reduction_median']*100:.2f}%\n"
         f"- Std Dev: {data_summary['churn_reduction_std']*100:.2f}%\n"
         f"- Range: {data_summary['churn_reduction_min']*100:.1f}% - {data_summary['churn_reduction_max']*100:.1f}%\n\n"
         f"Reduction in resident turnover/churn"
) / 100
efficiency_improvement = st.sidebar.slider(
    "Agent Efficiency Improvement (%)",
    min_value=10,
    max_value=35,
    value=int(data_summary['avg_efficiency_improvement'] * 100),
    help=f"**From Data:** Funnel assumptions sheet\n\n"
         f"- Value: **{data_summary['avg_efficiency_improvement']*100:.0f}%** (constant)\n"
         f"- Std Dev: {data_summary['efficiency_std']*100:.2f}%\n\n"
         f"Improvement in agent productivity\n"
         f"(same staff handles more units)"
) / 100

st.sidebar.markdown("---")

# Scenario Selection - Conservative as default
st.sidebar.markdown("### Scenario")
scenario = st.sidebar.radio(
    "Select Scenario",
    ["Conservative (50%)", "Base Case (100%)", "Optimistic (150%)"],
    index=0,  # Conservative as default
    help="**Scenario Multiplier**\n\n"
         "Scales all benefit calculations:\n\n"
         "- **Conservative (50%)**: Half of projected benefits"
         "- **Base Case (100%)**: Full projected benefits from data\n"
         "- **Optimistic (150%)**: 1.5x projected benefits"
)
scenario_multiplier = {"Conservative (50%)": 0.5, "Base Case (100%)": 1.0, "Optimistic (150%)": 1.5}[scenario]

# Staffing calculations using actual data
total_staff = int(data_summary['total_onsite_staff'])
monthly_leasing_hours = data_summary['total_monthly_leasing_hours']  # From actual data

# =============================================================================
# CALCULATIONS (Conservative Methodology)
# =============================================================================

# Portfolio Metrics
annual_revenue = total_units * avg_rent * occupancy_rate * 12
annual_leases = int(total_units * turnover_rate)
daily_rent = avg_rent / 30

# Value Driver 1: Conversion Improvement (CONSERVATIVE: Reduced vacancy time, not full lease value)
# Units would eventually be leased - benefit is faster leasing = less vacancy
additional_leases = annual_leases * conversion_lift * scenario_multiplier
# Conservative: value is reduced vacancy time, not entire annual rent
conversion_benefit = additional_leases * vacancy_days_saved * daily_rent

# Value Driver 2: Churn Reduction
turnovers_avoided = annual_leases * churn_reduction * scenario_multiplier
turnover_savings = turnovers_avoided * cost_per_turnover
vacancy_savings = turnovers_avoided * vacancy_days * daily_rent
retention_benefit = turnover_savings + vacancy_savings

# Value Driver 3: Labor Efficiency (using actual hours from data)
annual_leasing_hours = monthly_leasing_hours * 12
hours_saved = annual_leasing_hours * efficiency_improvement * scenario_multiplier
labor_benefit = hours_saved * hourly_wage

# Marketing Efficiency - SOFT BENEFIT (not included in ROI calculation)
leads_per_lease = data_summary['total_monthly_leads'] * 12 / annual_leases
marketing_cpl = 35  # Industry average
marketing_soft_benefit = additional_leases * leads_per_lease * marketing_cpl * 0.5

# Total Benefits (excludes marketing - noted separately as soft benefit)
total_benefit = conversion_benefit + retention_benefit + labor_benefit

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

# Header with Funnel Logo
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.markdown("""
        <img src="https://cdn-ikppojb.nitrocdn.com/ixIKpewMJHrrHCmWnougzUiFrykLuTxb/assets/images/optimized/rev-1cc0d03/funnelleasing.com/wp-content/themes/funnel-theme/public/images/logo.svg"
        style="width: 180px; margin-top: 10px;">
    """, unsafe_allow_html=True)
with col_title:
    st.markdown('<p class="main-header">Funnel Intelligence Bundle</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">ROI Business Case Analysis | {total_units:,}-Unit Owner-Operator Portfolio | {scenario}</p>', unsafe_allow_html=True)
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
        delta="Quick payback" if payback_months < 6 else "Standard",
        delta_color="normal" if payback_months < 6 else "off"
    )

st.markdown("---")

# =============================================================================
# TABS
# =============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Executive Summary",
    "Value Drivers",
    "Financial Model",
    "Sensitivity Analysis",
    "Stakeholder Views",
    "Data Quality"
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
        - **Faster Leasing** - {conversion_lift*100:.1f}% improvement reduces vacancy time
        - **Better Retention** - {churn_reduction*100:.1f}% reduction in resident churn
        - **Operational Efficiency** - {efficiency_improvement*100:.0f}% improvement in agent productivity
        """)

        st.markdown("### The Recommendation")

        if roi_percentage > 200:
            recommendation = "**STRONG BUY** - Excellent ROI with solid payback"
            color = "green"
        elif roi_percentage > 100:
            recommendation = "**BUY** - Strong ROI justifies investment"
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
            in annual net benefit per unit. The investment pays for itself in <strong>{payback_months:.1f} months</strong>.<br><br>
            <em>Note: This analysis uses conservative methodology - conversion benefit calculated as reduced vacancy time rather than full lease value.</em>
        </div>
        """, unsafe_allow_html=True)

        # Soft benefits callout
        st.markdown(f"""
        <div class="soft-benefit-box">
            <strong>Additional Soft Benefits (not included in ROI):</strong><br>
            Marketing Efficiency: <strong>${marketing_soft_benefit:,.0f}/year</strong> potential value from improved conversion reducing cost-per-lease.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Donut chart for value distribution (3 drivers only)
        fig = go.Figure(data=[go.Pie(
            labels=['Faster Leasing', 'Retention', 'Labor Efficiency'],
            values=[conversion_benefit, retention_benefit, labor_benefit],
            hole=.6,
            marker_colors=['#E91E8C', '#00C853', '#FFA726']
        )])
        fig.update_layout(
            title="Annual Benefit Distribution",
            showlegend=True,
            height=350,
            margin=dict(t=50, b=0, l=0, r=0)
        )
        fig.add_annotation(
            text=f"${total_benefit/1e6:.2f}M/yr",
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
    st.markdown(f"*{scenario} - All benefits scaled by {scenario_multiplier*100:.0f}%*")

    col1, col2 = st.columns([1, 1])

    with col1:
        # Bar chart (3 value drivers)
        fig = go.Figure(data=[
            go.Bar(
                x=['Faster Leasing', 'Retention', 'Labor Efficiency'],
                y=[conversion_benefit, retention_benefit, labor_benefit],
                marker_color=['#E91E8C', '#00C853', '#FFA726'],
                text=[f'${v/1e6:.2f}M' if v >= 1e6 else f'${v/1e3:.0f}K' for v in [conversion_benefit, retention_benefit, labor_benefit]],
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
        **1. Faster Leasing (Reduced Vacancy): ${conversion_benefit:,.0f}/year**
        - Additional leases from improved conversion: {additional_leases:,.0f}
        - Vacancy days saved per lease: {vacancy_days_saved} days
        - Daily rent value: ${daily_rent:,.0f}
        - *Conservative: Units would lease eventually; benefit is faster fill time*

        **2. Churn Reduction: ${retention_benefit:,.0f}/year**
        - Turnovers avoided: {turnovers_avoided:,.0f}
        - Turnover cost savings: ${turnover_savings:,.0f}
        - Vacancy loss avoided: ${vacancy_savings:,.0f}

        **3. Labor Efficiency: ${labor_benefit:,.0f}/year**
        - Current annual leasing hours: {annual_leasing_hours:,.0f}
        - Hours saved ({efficiency_improvement*100:.0f}%): {hours_saved:,.0f}
        - At {hourly_wage}/hour = ${labor_benefit:,.0f}
        - Enabled by our centralization strategy
        """)

        st.markdown(f"""
        <div class="soft-benefit-box">
            <strong>Soft Benefit: Marketing Efficiency</strong><br>
            Potential value: <strong>${marketing_soft_benefit:,.0f}/year</strong><br>
            Better conversion = lower cost per lease. Not included in ROI to avoid double-counting with conversion benefit.
        </div>
        """, unsafe_allow_html=True)

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
    st.markdown(f"*{scenario}*")

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
            'Metric': ['Faster Leasing Benefit', 'Retention Benefit', 'Labor Efficiency', 'Total Annual Benefit', 'Total Annual Cost', 'Net Annual Benefit', 'ROI', 'Payback Period'],
            'Value': [
                f'${conversion_benefit:,.0f}',
                f'${retention_benefit:,.0f}',
                f'${labor_benefit:,.0f}',
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
    fig.add_trace(go.Scatter(x=years, y=cumulative_cost, name='Cumulative Cost', line=dict(color='#FF5252', width=3)))
    fig.add_trace(go.Scatter(x=years, y=cumulative_net, name='Cumulative Net', line=dict(color='#E91E8C', width=3), fill='tozeroy'))

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
        <strong>5-Year Total Value ({scenario}):</strong><br>
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

    # Calculate scenarios using conservative methodology
    scenarios_data = []
    for mult, name in [(0.5, 'Conservative'), (1.0, 'Base Case'), (1.5, 'Optimistic')]:
        s_additional_leases = annual_leases * conversion_lift * mult
        s_conv = s_additional_leases * vacancy_days_saved * daily_rent  # Conservative: vacancy savings
        s_ret = (annual_leases * churn_reduction * mult * cost_per_turnover) + (annual_leases * churn_reduction * mult * vacancy_days * daily_rent)
        s_lab = annual_leasing_hours * efficiency_improvement * mult * hourly_wage
        s_total = s_conv + s_ret + s_lab  # No marketing
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
            go.Bar(name='Total Benefit', x=scenarios_df['Scenario'], y=scenarios_df['Total Benefit'], marker_color='#42A5F5'),
            go.Bar(name='Net Benefit', x=scenarios_df['Scenario'], y=scenarios_df['Net Benefit'], marker_color='#E91E8C')
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
        <div class="highlight-box">
            We present the <strong>Conservative scenario</strong> as our primary recommendation.
            Even at 50% of projected benefits, the investment delivers strong positive ROI.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Single variable sensitivity
    st.markdown("### Single Variable Sensitivity")

    # Calculate base benefits for sensitivity (using 100% multiplier)
    base_conversion_benefit = annual_leases * conversion_lift * vacancy_days_saved * daily_rent
    base_retention_benefit = (annual_leases * churn_reduction * cost_per_turnover) + (annual_leases * churn_reduction * vacancy_days * daily_rent)
    base_labor_benefit = annual_leasing_hours * efficiency_improvement * hourly_wage

    sensitivity_var = st.selectbox(
        "Select variable to analyze:",
        ["Conversion Improvement", "Churn Reduction", "Efficiency Improvement", "Funnel Price", "Vacancy Days Saved"]
    )

    if sensitivity_var == "Conversion Improvement":
        var_range = [x/100 for x in range(1, 16)]
        var_label = "Conversion Improvement (%)"
        results = []
        for v in var_range:
            s_conv = annual_leases * v * vacancy_days_saved * daily_rent
            s_total = s_conv + base_retention_benefit + base_labor_benefit
            results.append({'Variable': v*100, 'Net Benefit': s_total - annual_cost})

    elif sensitivity_var == "Churn Reduction":
        var_range = [x/100 for x in range(1, 11)]
        var_label = "Churn Reduction (%)"
        results = []
        for v in var_range:
            s_ret = (annual_leases * v * cost_per_turnover) + (annual_leases * v * vacancy_days * daily_rent)
            s_total = base_conversion_benefit + s_ret + base_labor_benefit
            results.append({'Variable': v*100, 'Net Benefit': s_total - annual_cost})

    elif sensitivity_var == "Efficiency Improvement":
        var_range = [x/100 for x in range(10, 36, 5)]
        var_label = "Efficiency Improvement (%)"
        results = []
        for v in var_range:
            s_lab = annual_leasing_hours * v * hourly_wage
            s_total = base_conversion_benefit + base_retention_benefit + s_lab
            results.append({'Variable': v*100, 'Net Benefit': s_total - annual_cost})

    elif sensitivity_var == "Vacancy Days Saved":
        var_range = list(range(5, 31, 5))
        var_label = "Vacancy Days Saved per Lease"
        results = []
        for v in var_range:
            s_conv = annual_leases * conversion_lift * v * daily_rent
            s_total = s_conv + base_retention_benefit + base_labor_benefit
            results.append({'Variable': v, 'Net Benefit': s_total - annual_cost})

    else:  # Funnel Price
        var_range = [x/10 for x in range(20, 60, 5)]
        var_label = "Funnel Price ($/unit/month)"
        results = []
        for v in var_range:
            s_cost = total_units * v * 12
            s_total = base_conversion_benefit + base_retention_benefit + base_labor_benefit
            results.append({'Variable': v, 'Net Benefit': s_total - s_cost})

    results_df = pd.DataFrame(results)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=results_df['Variable'],
        y=results_df['Net Benefit'],
        mode='lines+markers',
        line=dict(color='#E91E8C', width=3),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title=f"Net Benefit Sensitivity to {sensitivity_var}",
        xaxis_title=var_label,
        yaxis_title="Net Annual Benefit ($)",
        height=400
    )
    # Add reference line at base case value
    base_net_benefit = base_conversion_benefit + base_retention_benefit + base_labor_benefit - annual_cost
    fig.add_hline(y=base_net_benefit, line_dash="dash", line_color="#00C853",
                  annotation_text=f"Base Case: ${base_net_benefit:,.0f}")
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 5: STAKEHOLDER VIEWS
# =============================================================================
with tab5:
    st.markdown("## Stakeholder Perspectives")
    st.markdown(f"*{scenario}*")

    stakeholder = st.radio(
        "Select Stakeholder View:",
        ["Financial", "Marketing", "Operations"],
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
            st.metric("Payback", f"{payback_months:.1f} months", "Quick" if payback_months < 6 else "Standard")

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

        ### Critical Features
        - Investment pays for itself in {payback_months:.1f} months
        - {roi_percentage:,.0f}% ROI using conservative methodology
        - Operating expense (not CapEx) - ${funnel_price:.2f}/unit/month
        - Scales with portfolio - costs aligned with revenue
        - Analysis excludes marketing efficiency (~${marketing_soft_benefit:,.0f} additional soft benefit)
        """)

    elif stakeholder == "VP of Marketing":
        st.markdown("### VP of Marketing View: Lead Performance")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Faster Lease-ups", f"{additional_leases:,.0f}/yr", f"+{conversion_lift*100:.1f}% conversion")
        with col2:
            st.metric("Reduced Vacancy", f"{int(additional_leases * vacancy_days_saved):,} days", f"${conversion_benefit:,.0f} value")
        with col3:
            st.metric("Lead Response", "24/7", "AI-powered")

        st.markdown(f"""
        ### Marketing Impact

        | Metric | Current | With Funnel | Improvement |
        |--------|---------|-------------|-------------|
        | Lead Response Time | Variable | <5 minutes | Instant 24/7 |
        | Lead-to-Lease Conversion | Baseline | +{conversion_lift*100:.1f}% | {additional_leases:,.0f} faster leases |
        | Inquiry Handling | Manual | 80% automated | AI-powered |
        | Attribution | Limited | Multi-touch | Full visibility |

        ### Features for Marketing
        - **Prospect AI** - Handles 80% of initial inquiries automatically
        - **AI Chatbot** - Website engagement, lead capture
        - **Multi-touch Attribution** - Know which channels drive leases
        - **Cross-selling** - 800 bps improvement in referrals
        - **ILS Syndication** - Optimized listings across platforms

        ### Marketing Value
        - {additional_leases:,.0f} faster leases = {int(additional_leases * vacancy_days_saved):,} fewer vacancy days
        - Vacancy value recovered: ${conversion_benefit:,.0f}
        - Soft benefit from lower cost-per-lease: ~${marketing_soft_benefit:,.0f} (not in ROI)
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
            st.metric("Agent Ratio", f"{units_per_staff}:1 -> {new_ratio:.0f}:1", "Centralization enabled")

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
# TAB 6: DATA QUALITY
# =============================================================================
with tab6:
    st.markdown("## Data Quality Summary")

    st.markdown("""
    This analysis is based on actual portfolio data provided in the case study dataset.
    Below is a summary of data quality and any cleaning performed.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Dataset Overview")
        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | Total Properties | {data_summary['total_properties']:,} |
        | Total Units | {data_summary['total_units']:,} |
        | Data Sheets | 4 (properties, performance, staffing, assumptions) |
        """)

        st.markdown("### Key Metrics from Data")
        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | Average Rent (mean) | ${data_summary['avg_rent']:,.0f} |
        | Average Rent (median) | ${data_summary['avg_rent_median']:,.0f} |
        | Total Monthly Leads | {data_summary['total_monthly_leads']:,} |
        | Average Contact Rate | {data_summary['avg_contact_rate']*100:.1f}% |
        | Total Onsite Staff | {data_summary['total_onsite_staff']:,} |
        | Monthly Leasing Hours | {data_summary['total_monthly_leasing_hours']:,.0f} |
        """)

    with col2:
        st.markdown("### Missing Data Handling")

        missing_info = data_summary['missing_info']
        st.markdown(f"""
        <div class="data-quality-box">
            <strong>Missing Values (filled with median):</strong><br>
            - contact_rate: {missing_info['contact_rate']} values<br>
            - avg_rent: {missing_info['avg_rent']} values<br>
            - leasing_staff_hours: {missing_info['leasing_staff_hours']} values<br><br>
            <em>All missing values filled with column median - standard practice for numerical data.</em>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Funnel Assumptions from Data")
        st.markdown(f"""
        | Assumption | Mean | Range |
        |------------|------|-------|
        | Conversion Lift | {data_summary['avg_conversion_lift']*100:.2f}% | 4-10% |
        | Churn Reduction | {data_summary['avg_churn_reduction']*100:.2f}% | 1-6% |
        | Efficiency Improvement | {data_summary['avg_efficiency_improvement']*100:.0f}% | 20% (constant) |
        """)

    st.markdown("---")

    st.markdown("### Methodology Notes")
    st.markdown("""
    <div class="warning-box">
        <strong>Conservative Methodology Applied:</strong><br><br>
        <strong>1. Conversion Benefit:</strong> Calculated as <em>reduced vacancy time</em> rather than full lease value.
        Rationale: Units would eventually be leased; the benefit is faster fill time, not incremental revenue.<br><br>
        <strong>2. Marketing Efficiency:</strong> Excluded from ROI calculation and noted as a "soft benefit" to avoid
        double-counting with conversion improvement.<br><br>
        <strong>3. Scenario Default:</strong> Conservative (50%) scenario presented as primary recommendation.<br><br>
        <strong>4. Data-Driven Defaults:</strong> All model defaults (rent, staffing, conversion rates) loaded from actual
        portfolio data rather than industry assumptions.
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p><strong>Funnel Intelligence Bundle - ROI Analysis Dashboard</strong></p>
    <p>Data-driven analysis for {total_units:,}-unit owner-operator portfolio</p>
    <p>Conservative methodology | Defaults from actual portfolio data | {scenario}</p>
</div>
""", unsafe_allow_html=True)

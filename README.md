# Funnel Intelligence Bundle - ROI Business Case

## 19,000-Unit Owner-Operator Portfolio Analysis

---

## Quick Start

### Live Demo
Access the live dashboard at: [Coming soon - will be deployed on Streamlit Cloud]

### Run Locally
**Option 1: Run the Interactive Dashboard**
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```
Then open http://localhost:8501 in your browser.

**Option 2: View the Presentation**
Open `presentation/index.html` directly in your browser.

---

## Deliverables

### 1. Interactive Dashboard (`dashboard/app.py`)
A fully interactive Streamlit application featuring:

**Tunable Assumptions (Sidebar):**
- Portfolio: Units, Rent, Occupancy, Turnover Rate
- Costs: Turnover Cost, Vacancy Days, Hourly Wage, Marketing CPL
- Funnel: Price/unit, Conversion Lift, Churn Reduction, Efficiency %
- Scenario Toggle: Conservative/Base/Optimistic

**Dashboard Tabs:**
1. **Executive Summary** - Key metrics, recommendation, benefit distribution
2. **Value Drivers** - Detailed breakdown of all four value drivers
3. **Financial Model** - Investment, returns, 5-year projection
4. **Sensitivity Analysis** - Scenario comparison, single-variable analysis
5. **Stakeholder Views** - CFO, VP Marketing, SVP Operations perspectives

### 2. HTML Presentation (`presentation/index.html`)
A 7-slide reveal.js presentation covering:
1. Title Slide
2. The Opportunity (Portfolio + Challenge)
3. The Solution (Funnel Features)
4. Four Value Drivers
5. Financial Summary
6. Stakeholder Value
7. Recommendation & Next Steps
8. Appendix (Assumptions)

**Navigation:** Use arrow keys or click to advance slides.

### 3. Analysis Documents
- `FINAL_Analysis_Summary.md` - Complete written analysis with pushback responses
- `Funnel_Resources_Comprehensive_Summary.md` - Research summary
- `ROI_Summary_v2.csv` - Key metrics for Excel/Sheets
- `Value_Drivers_v2.csv` - Value driver breakdown

### 4. Python Analysis Scripts
- `funnel_roi_analysis_v2.py` - Full ROI calculation script
- `read_excel_data.py` - Data extraction script

---

## Key Results

| Metric | Value |
|--------|-------|
| **Annual Investment** | $843,600 |
| **Total Annual Benefit** | $21,123,604 |
| **Net Annual Benefit** | $20,280,004 |
| **ROI** | 2,404% |
| **Payback Period** | 0.5 months |

### Value Drivers

| Driver | Annual Benefit | % of Total |
|--------|----------------|------------|
| Conversion Improvement | $14,515,581 | 68.7% |
| Labor Efficiency | $4,278,437 | 20.3% |
| Churn Reduction | $1,931,011 | 9.1% |
| Marketing Efficiency | $398,575 | 1.9% |

---

## Presentation Flow (Recommended)

### For Client Meeting:

1. **Start with HTML Presentation** (10-15 min)
   - Walk through the 7 slides
   - Cover the story: opportunity → solution → value → recommendation

2. **Switch to Interactive Dashboard** (15-20 min)
   - Show real-time calculations
   - Adjust assumptions based on client's actual data
   - Explore stakeholder-specific views
   - Run sensitivity analysis

3. **Address Questions with Dashboard**
   - "What if our turnover is different?" → Adjust slider
   - "What if we only achieve 50%?" → Switch to conservative scenario
   - "What does this mean for my team?" → Show SVP Operations view

---

## File Structure

```
Funnel Leasing/
├── run_dashboard.bat           # Launch interactive dashboard
├── run_presentation.bat        # Open HTML presentation
├── README.md                   # This file
│
├── dashboard/
│   ├── app.py                  # Streamlit dashboard
│   └── requirements.txt        # Python dependencies
│
├── presentation/
│   └── index.html              # Reveal.js slides
│
├── venv/                       # Python virtual environment
│
├── FINAL_Analysis_Summary.md   # Complete analysis document
├── Funnel_Resources_Comprehensive_Summary.md
├── ROI_Summary_v2.csv
├── Value_Drivers_v2.csv
├── funnel_roi_analysis_v2.py
│
└── Value Engineer _ Case Study Data.xlsx  # Source data
```

---

## Technical Requirements

- Python 3.11+
- Modern web browser (Chrome, Edge, Firefox)
- Dependencies listed in `requirements.txt`

---

## Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your GitHub account
4. Deploy from `dashboard/app.py`
5. Share the public URL

### Alternative Platforms
- **Heroku**: Add `Procfile` and `setup.sh`
- **Railway**: Direct deployment from GitHub
- **Render**: Use web service with Python environment

---

## Customization

### To adjust default values:
Edit `dashboard/app.py` and modify the `st.sidebar` input default values.

### To modify the presentation:
Edit `presentation/index.html` - it's a standard HTML file with reveal.js.

### To regenerate analysis:
Run `funnel_roi_analysis_v2.py` with the venv Python.

---

## Support

For questions about the analysis methodology, refer to:
- `FINAL_Analysis_Summary.md` - Includes assumptions, methodology, and pushback responses
- `Funnel_Resources_Comprehensive_Summary.md` - Funnel product research

---

**Created:** January 2026
**Analysis Period:** 12 months
**Portfolio:** 19,000 units | 400 properties

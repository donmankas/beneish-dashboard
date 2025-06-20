"""
Created on Thu Jun 19 16:12:20 2025

@author: manakkashyap
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide", page_title="📊 Beneish Full Dashboard")
st.title("📊 Full Beneish M-Score and Deviation Analysis Dashboard")

st.markdown("""
This dashboard analyzes **earnings manipulation risk** using the **Beneish M-Score model**.
We use the following 8 financial ratios:

| Ratio | Meaning | Signal | 
|-------|---------|--------|
| **DSRI** | Days' Sales in Receivables Index | Revenue inflation risk |
| **GMI** | Gross Margin Index | Margin deterioration risk |
| **AQI** | Asset Quality Index | Inflated/intangible assets risk |
| **SGI** | Sales Growth Index | Growth-driven manipulation |
| **DEPI** | Depreciation Index | Slower depreciation inflates profit |
| **SGAI** | SG&A Expense Index | Admin cost underreporting |
| **TATA** | Total Accruals to Total Assets | High accruals risk |
| **LVGI** | Leverage Index | Risk from increasing leverage |

📌 We apply **sector-specific logic**:
- **Healthcare**: Adjust AQI for R&D; flag if AQI & GMI both rise
- **Utilities**: High AQI (>2.5) is normal ➝ downweight
- **Consumer Cyclical**: Smooth SGI via rolling average
- **Real Estate**: Treat revenue swings as norm; flag DSRI + SGI only if >2
- **Technology**: If DEPI < 1 and TATA > 0 ➝ flag as cash flow mismatch

The model flags companies based on:
- **M-Score < –2.22** ➝ ✅ Safe
- **–2.22 to –1.78** ➝ ⚠️ Watchlist
- **> –1.78** ➝ 🚩 Red Flag
### 🧠 Sector-Specific Adjustments

- **Healthcare**: R&D-heavy → AQI inflation is common. A red flag only if AQI **and** GMI both rise.
- **Utilities**: High AQI (>2.5) is typical due to asset nature → downweighted in scoring.
- **Consumer Cyclical**: Volatile sales → SGI smoothed using 2-year average.
- **Real Estate**: Revenue recognition via milestones → DSRI + SGI only flagged if **both > 2**.
- **Technology**: Cash flow analysis critical → DEPI < 1 **and** TATA > 0 = likely manipulation.

### 📊 Deviation Score (Volatility Logic)

For each ratio:
- Compute **Z-score** = (Company Ratio – Sector-Year Mean) / Sector-Year Std Dev
- Then take **Average Z across 8 ratios**

This yields:
- **Stable**: Avg Z < 0.5
- **Mid-Risk**: 0.5 ≤ Avg Z < 1.0
- **Volatile**: Avg Z ≥ 1.0

These scores are used to:
- Rank company consistency
- Suggest balanced portfolio picks
- Highlight dangerous outliers


📈 Use the tabs below for analysis across trends, flags, deviations, portfolio suggestions, and filtering.
""")

# Load Data
data_summary = pd.read_excel("/Users/manakkashyap/Desktop/spyder/SECTOR_ANALYSIS/beneish_sector_summary_sector.xlsx")
data_full = pd.read_excel("/Users/manakkashyap/Desktop/spyder/SECTOR_ANALYSIS/beneish_full_ratio_status_sector.xlsx")
data_flags = pd.read_excel("/Users/manakkashyap/Desktop/spyder/SECTOR_ANALYSIS/beneish_flag_breakdown_by_sector.xlsx")
data_deviation = pd.read_excel("/Users/manakkashyap/Desktop/spyder/SECTOR_ANALYSIS/sector_company_deviation_analysis_full.xlsx", sheet_name="Stability_Ranking")
data_top_stable = pd.read_excel("/Users/manakkashyap/Desktop/spyder/SECTOR_ANALYSIS/sector_company_deviation_analysis_full.xlsx", sheet_name="Top_20_Stable")
data_top_volatile = pd.read_excel("/Users/manakkashyap/Desktop/spyder/SECTOR_ANALYSIS/sector_company_deviation_analysis_full.xlsx", sheet_name="Top_20_Volatile")
data_deviation_types = pd.read_excel("/Users/manakkashyap/Desktop/spyder/SECTOR_ANALYSIS/sector_company_deviation_analysis_full.xlsx", sheet_name="Significant_Deviations")
data_portfolio = pd.read_excel("/Users/manakkashyap/Desktop/spyder/SECTOR_ANALYSIS/final_portfolio_suggestion.xlsx")

T1, T2, T3, T4, T5, T6, T7, T8, T9 = st.tabs([
    "📈 Sector M-Score Trends",
    "🔥 Red Flags Overview",
    "📋 Full Company Ratios",
    "🧠 Deviation Summary",
    "🏆 Top Stable vs Volatile",
    "📊 Deviation Type Highlights",
    "💼 Final Portfolio Picks",
    "🔍 Filter & Explore",
    "🧾 Company Deep Dive"
])


with T1:
    st.subheader("📈 Average M-Score by Sector and Year")
    fig1 = px.line(data_summary, x="Year", y="Avg M-Score", color="Sector", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🌡️ Heatmap of Sector M-Scores")
    heatmap_data = data_summary.pivot(index='Sector', columns='Year', values='Avg M-Score')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap='RdYlGn_r', center=-2.22, ax=ax)
    st.pyplot(fig)

with T2:
    st.subheader("🔥 Red Flag Status Summary")
    st.dataframe(data_flags)

with T3:
    st.subheader("📋 Company-Level Beneish Ratio Data")
    st.dataframe(data_full, use_container_width=True)

with T4:
    st.subheader("🧠 Company Deviation Scores vs Sector")
    st.dataframe(data_deviation)

with T5:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Top 20 Most Stable Companies")
        st.dataframe(data_top_stable)
    with col2:
        st.subheader("⚠️ Top 20 Most Volatile Companies")
        st.dataframe(data_top_volatile)

with T6:
    st.subheader("🔬 Largest Ratio Deviations (Z-Score > 2)")
    st.dataframe(data_deviation_types, use_container_width=True)

with T7:
    st.subheader("💼 Suggested Final Portfolio (Diversified)")
    st.markdown("Includes Stable, Moderate, and Volatile companies with 'Safe' or 'Watchlist' M-Scores")
    st.dataframe(data_portfolio, use_container_width=True)

with T8:
    st.subheader("🔍 Filter Companies by Sector, M-Score, or Stability")
    sector_choice = st.selectbox("Select Sector:", ["All"] + sorted(data_full["Sector"].dropna().unique().tolist()))
    mscore_range = st.slider("M-Score Range", -6.0, 3.0, (-5.0, -2.0))
    filtered_data = data_full[
        (data_full["M-Score"] >= mscore_range[0]) &
        (data_full["M-Score"] <= mscore_range[1])
    ]
    if sector_choice != "All":
        filtered_data = filtered_data[filtered_data["Sector"] == sector_choice]
    st.dataframe(filtered_data, use_container_width=True)

    st.subheader("📊 M-Score vs. Market Cap")
    if "Market Cap (Cr)" in data_full.columns:
        fig = px.scatter(
            filtered_data,
            x="Market Cap (Cr)",
            y="M-Score",
            color="Sector",
            hover_data=["Ticker", "Status"],
            title="🧠 Safe vs Undervalued View"
        )
        st.plotly_chart(fig, use_container_width=True)
with T9:
    st.subheader("🧾 Deep Dive into a Company by Sector")
    
    sector_selected = st.selectbox("📂 Select a Sector", sorted(data_full["Sector"].dropna().unique()))
    stock_options = data_full[data_full["Sector"] == sector_selected]["Ticker"].dropna().unique()
    stock_selected = st.selectbox("🏷️ Select a Company", sorted(stock_options))

    company_info = data_full[(data_full["Sector"] == sector_selected) & (data_full["Ticker"] == stock_selected)]
    deviation_info = data_deviation[data_deviation["Ticker"] == stock_selected]

    st.markdown(f"### 🏢 Detailed Ratios and Status for `{stock_selected}`")
    st.dataframe(company_info.transpose(), use_container_width=True)

    st.markdown(f"### 📊 Deviation Score Compared to Sector")
    if not deviation_info.empty:
        st.dataframe(deviation_info.transpose(), use_container_width=True)
    else:
        st.warning("No deviation data available for this company.")

    st.markdown("### ⚠️ Sector-Specific Notes or Flags")
    notes = ""
    sector = sector_selected
    row = company_info.iloc[0]
    
    if sector == "Healthcare":
        if row["AQI"] > 1 and row["GMI"] > 1:
            notes = "📌 *High AQI & GMI — Possible R&D capitalization concerns.*"
    elif sector == "Utilities":
        if row["AQI"] > 2.5:
            notes = "ℹ️ *High AQI is typical — downweighted.*"
    elif sector == "Consumer Cyclical":
        notes = "🌀 *SGI smoothed using rolling average — watch large swings.*"
    elif sector == "Real Estate":
        if row["DSRI"] > 2 and row["SGI"] > 2:
            notes = "🚩 *High DSRI & SGI — caution due to revenue volatility.*"
    elif sector == "Technology":
        if row["DEPI"] < 1 and row["TATA"] > 0:
            notes = "⚠️ *DEPI < 1 with positive TATA — cash flow mismatch risk.*"

    if notes:
        st.info(notes)
    else:
        st.success("No special sector-based red flags identified.")

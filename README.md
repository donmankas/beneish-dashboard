# 📊 Beneish Dashboard: NSE Forensic Analysis (2019–2025)

This project uses the **Beneish M-Score model** combined with **Z-Score stability analysis** to identify companies with potential earnings manipulation across NSE-listed firms between 2019 and 2025.

Built with **Streamlit**, this interactive dashboard allows you to explore:
- 📉 Beneish ratio trends (DSRI, SGI, AQI, etc.)
- 📊 Company vs. Sector Z-score deviations
- 🚨 Red flag combinations (e.g., SGI + DSRI > 2)
- ✅ Stability ranking and portfolio suggestions

---

## ⚙️ How to Run the Dashboard Locally

1. Install Streamlit:

   ```bash
   pip install streamlit

2.Clone this repository

git clone https://github.com/donmankas/beneish-dashboard.git
cd beneish-dashboard

3.Run the dashboard:

streamlit run beneish_dashboard_3.py

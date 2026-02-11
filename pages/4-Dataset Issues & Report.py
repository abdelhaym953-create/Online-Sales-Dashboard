import streamlit as st
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html

#================= PAGE CONFIG =================
st.set_page_config(page_title="Online Sales Dashboard", layout="wide",page_icon='online-shop_164427.png')

st.title("📊 Dataset Issues & Data Quality Report")
st.markdown("A concise review of dataset structure and reliability.")

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = pd.read_csv("online_sales_dataset.csv")

total_rows = df.shape[0]
total_cols = df.shape[1]
missing_total = df.isna().sum().sum()
duplicate_count = df.duplicated().sum()

missing_percent = (missing_total / (total_rows * total_cols)) * 100
duplicate_percent = (duplicate_count / total_rows) * 100

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.subheader("📌 Dataset KPIs ")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{total_rows:,}")
col2.metric("Total Columns", total_cols)
col3.metric("Missing Data %", f"{missing_percent:.2f}%")
col4.metric("Duplicate Records %", f"{duplicate_percent:.2f}%")

st.divider()

# -------------------------------------------------
# Hidden but Smart Observations
# -------------------------------------------------
st.subheader("🔎 Structural Observations")

st.markdown("""
Minor gaps, limited duplicates, and a few extreme values were identified during exploration.  
These were reviewed to ensure KPI accuracy.
""")
st.divider()

# -------------------------------------------------
# Data Reliability Assessment
# -------------------------------------------------
st.subheader("🎯 Data Reliability Assessment")

st.markdown("""
The dataset is structurally consistent and suitable for performance analysis.
""")

st.divider()

# -------------------------------------------------
# Optional Profiling Report
# -------------------------------------------------
st.subheader("📘 Advanced Technical Details")

if st.checkbox("🔍 View Full Profiling Report"):
    profile = ProfileReport(df, explorative=True)
    profile_html = profile.to_html()
    html(profile_html, height=900, scrolling=True)

# ================= FOOTER =================
st.markdown("---")
st.caption(" Developed by Eng. Mohamed 🚀📊")
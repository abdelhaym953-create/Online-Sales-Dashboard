import pandas as pd
import plotly.express as px
import streamlit as st





# ================= Page Config =================

st.set_page_config(page_title="Online Sales Dashboard", layout="wide",page_icon='online-shop_164427.png')


# ================= Load Data =================
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_dataset.csv")

df = load_data()

# ================= Column Groups =================
num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
exclude_cols = ["CustomerID", "InvoiceNo"]

# Only categorical columns with <50 unique values, excluding IDs
cat_cols = [c for c in df.select_dtypes(include="object").columns
            if c not in exclude_cols and df[c].nunique() < 50]

date_col = "invoicedate"

# ================= Title =================
st.title("📊 Bivariate Analysis Dashboard")
st.markdown("Analyze relationships between two variables.")
st.divider()

# ================= Tabs =================
tab1, tab2, tab3 = st.tabs(
    ["🔢 Numeric vs Numeric", "🏷️ Category vs Numeric", "📅 Time vs Numeric"]
)

# =================================================
# 🔢 NUMERIC vs NUMERIC
# =================================================
with tab1:
    st.subheader("Numeric vs Numeric Analysis")

    # Pick only numeric columns that are not IDs
    num_cols_for_num = [c for c in num_cols if c not in exclude_cols]
    x_num = st.selectbox("X Variable", num_cols_for_num, key="num_x")
    y_num = st.selectbox("Y Variable", [c for c in num_cols_for_num if c != x_num], key="num_y")

    c1, c2, c3 = st.columns(3)
    corr = df[x_num].corr(df[y_num])

    c1.metric("Records", len(df))
    c2.metric("Correlation", "N/A" if pd.isna(corr) else f"{corr:.2f}")
    c3.metric(f"Avg {y_num}", f"{df[y_num].mean():,.2f}")

    fig = px.scatter(
        df,
        x=x_num,
        y=y_num,
        title=f"{x_num} vs {y_num}"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 💡 Insight")
    if pd.isna(corr):
        st.info("Not enough data to calculate correlation.")
    elif abs(corr) > 0.6:
        st.success("Strong relationship between the two variables.")
    elif abs(corr) > 0.3:
        st.info("Moderate relationship detected.")
    else:
        st.warning("Weak or no clear relationship.")

# =================================================
# 🏷️ CATEGORY vs NUMERIC
# =================================================
with tab2:
    st.subheader("Category vs Numeric Analysis")

    # Only meaningful categorical columns for grouping
    cat_cols_for_cat = [c for c in cat_cols if c != "invoicedate"]
    cat = st.selectbox("Category Variable", cat_cols_for_cat, key="cat_x")

    # Only numeric columns that make sense (exclude IDs, ratios, etc.)
    num_cols_for_cat = [c for c in num_cols if c not in exclude_cols and c not in ["Shipping_Ratio"]]
    metric = st.selectbox("Numeric Metric", num_cols_for_cat, key="cat_y")

    agg = st.radio("Aggregation", ["Mean", "Sum"], horizontal=True)

    try:
        if agg == "Sum":
            temp = df.groupby(cat)[metric].sum().reset_index()
        else:
            temp = df.groupby(cat)[metric].mean().reset_index()

        temp = temp.sort_values(metric, ascending=False)

        c1, c2 = st.columns(2)
        c1.metric("Categories", temp.shape[0])
        c2.metric("Top Category", temp.iloc[0, 0])

        fig = px.bar(
            temp,
            x=cat,
            y=metric,
            title=f"{agg} {metric} by {cat}",
            text=metric
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 💡 Insight")
        st.info(
            f"**{temp.iloc[0,0]}** has the highest {agg.lower()} "
            f"{metric} ({temp.iloc[0,1]:,.2f})."
        )
    except Exception as e:
        st.error(f"Error: {e}")

# =================================================
# 📅 TIME vs NUMERIC
# =================================================
with tab3:
    st.subheader("Time Trend Analysis")

    # Only numeric columns that are not IDs or ratios
    num_cols_for_time = [c for c in num_cols if c not in exclude_cols and c not in ["Shipping_Ratio"]]
    metric = st.selectbox("Numeric Metric", num_cols_for_time, key="time_y")

    agg = st.radio("Aggregation", ["Mean", "Sum"], horizontal=True, key="time_agg")

    temp = df.copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
    temp = temp.dropna(subset=[date_col])
    temp["Month"] = temp[date_col].dt.to_period("M").astype(str)

    if agg == "Sum":
        temp = temp.groupby("Month")[metric].sum().reset_index()
    else:
        temp = temp.groupby("Month")[metric].mean().reset_index()

    fig = px.line(
        temp,
        x="Month",
        y=metric,
        markers=True,
        title=f"{agg} {metric} Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 💡 Insight")
    st.info("This chart shows how the selected metric changes over time.")

# ================= Footer =================
st.markdown("---")
st.caption("Bivariate Analysis | Developed by Eng. Mohamed")

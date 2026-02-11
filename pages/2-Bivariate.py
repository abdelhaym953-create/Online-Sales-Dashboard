import pandas as pd
import plotly.express as px
import streamlit as st





# ================= Page Config =================

st.set_page_config(page_title="Online Sales Dashboard", layout="wide",page_icon='online-shop_164427.png')


# ================= Load Data =================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset.csv")

    # Fix duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # Convert numeric-like columns
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    return df


df = load_data()


# ==================================================
# COLUMN TYPES
# ==================================================

num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

cat_cols = [
    c for c in df.select_dtypes(include="object").columns
    if df[c].nunique() < 50
]

date_cols = [
    c for c in df.columns
    if "date" in c.lower() or "time" in c.lower()
]


# ==================================================
# HEADER
# ==================================================

st.title("📊 Bivariate Analysis Dashboard")

st.markdown("""
Analyze relationships between variables to discover patterns and trends.
""")

st.divider()


# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3 = st.tabs([
    "🔢 Numeric vs Numeric",
    "🏷️ Category vs Numeric",
    "📅 Time vs Numeric"
])


# ==================================================
# TAB 1 : NUMERIC vs NUMERIC
# ==================================================

with tab1:

    st.subheader("🔢 Numeric vs Numeric Analysis")

    if len(num_cols) < 2:
        st.warning("Not enough numeric columns.")
        st.stop()


    c1, c2, c3, c4 = st.columns(4)

    x_col = c1.selectbox(
        "X Variable",
        num_cols,
        key="num_x"
    )

    y_col = c2.selectbox(
        "Y Variable",
        [c for c in num_cols if c != x_col],
        key="num_y"
    )

    chart_type = c3.selectbox(
        "Chart Type",
        [
            "Correlation Scatter",
            "Regression Line",
            "Distribution View",
            "Density Heatmap"
        ],
        key="num_chart"
    )

    sample = c4.slider(
        "Sample Size",
        500,
        min(5000, len(df)),
        min(2000, len(df)),
        key="num_sample"
    )


    temp = df[[x_col, y_col]].dropna()

    if len(temp) > sample:
        temp = temp.sample(sample)


    # KPIs
    corr = temp[x_col].corr(temp[y_col])

    m1, m2, m3 = st.columns(3)

    m1.metric("Records", len(temp))
    m2.metric("Correlation", f"{corr:.2f}")
    m3.metric(f"Avg {y_col}", f"{temp[y_col].mean():,.2f}")


    # Charts
    if chart_type == "Correlation Scatter":

        fig = px.scatter(
            temp,
            x=x_col,
            y=y_col,
            trendline="ols",
            opacity=0.7
        )


    elif chart_type == "Regression Line":

        fig = px.scatter(
            temp,
            x=x_col,
            y=y_col,
            trendline="ols"
        )


    elif chart_type == "Distribution View":

        fig = px.scatter(
            temp,
            x=x_col,
            y=y_col,
            marginal_x="histogram",
            marginal_y="box"
        )


    else:  # Density

        fig = px.density_heatmap(
            temp,
            x=x_col,
            y=y_col
        )


    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)


    # Insight
    st.markdown("### 💡 Insight")

    if abs(corr) > 0.7:
        st.success("Strong relationship detected.")

    elif abs(corr) > 0.4:
        st.info("Moderate relationship exists.")

    else:
        st.warning("Weak or no clear relationship.")



# ==================================================
# TAB 2 : CATEGORY vs NUMERIC
# ==================================================

with tab2:

    st.subheader("🏷️ Category vs Numeric Analysis")

    if not cat_cols or not num_cols:
        st.warning("Not enough columns for this analysis.")
        st.stop()


    c1, c2, c3 = st.columns(3)

    cat = c1.selectbox(
        "Category",
        cat_cols,
        key="cat_x"
    )

    metric = c2.selectbox(
        "Metric",
        num_cols,
        key="cat_y"
    )

    agg = c3.radio(
        "Aggregation",
        ["Mean", "Sum", "Median"],
        horizontal=True,
        key="cat_agg"
    )


    if agg == "Sum":
        temp = df.groupby(cat)[metric].sum()

    elif agg == "Median":
        temp = df.groupby(cat)[metric].median()

    else:
        temp = df.groupby(cat)[metric].mean()


    temp = temp.round(2).reset_index()
    temp = temp.sort_values(metric, ascending=False)


    # KPIs
    m1, m2, m3 = st.columns(3)

    m1.metric("Categories", len(temp))
    m2.metric("Top Category", temp.iloc[0][cat])
    m3.metric("Top Value", f"{temp.iloc[0][metric]:,.2f}")


    # Chart
    fig = px.bar(
        temp,
        x=cat,
        y=metric,
        text=metric,
        title=f"{agg} {metric} by {cat}"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)


    # Insight
    st.markdown("### 💡 Insight")

    st.info(
        f"{temp.iloc[0][cat]} has the highest {agg.lower()} "
        f"({temp.iloc[0][metric]:,.2f})"
    )



# ==================================================
# TAB 3 : TIME vs NUMERIC
# ==================================================

with tab3:

    st.subheader("📅 Time Trend Analysis")


    if not date_cols:
        st.warning("No date column found.")
        st.stop()


    c1, c2, c3 = st.columns(3)

    date_col = c1.selectbox(
        "Date Column",
        date_cols,
        key="time_date"
    )

    metric = c2.selectbox(
        "Metric",
        num_cols,
        key="time_metric"
    )

    agg = c3.radio(
        "Aggregation",
        ["Mean", "Sum"],
        horizontal=True,
        key="time_agg"
    )


    temp = df.copy()

    temp[date_col] = pd.to_datetime(
        temp[date_col],
        errors="coerce"
    )

    temp = temp.dropna(subset=[date_col])


    temp["YearMonth"] = temp[date_col].dt.to_period("M").astype(str)


    if agg == "Sum":
        temp = temp.groupby("YearMonth", as_index=False)[metric].sum()

    else:
        temp = temp.groupby("YearMonth", as_index=False)[metric].mean()


    temp[metric] = temp[metric].round(2)


    fig = px.line(
        temp,
        x="YearMonth",
        y=metric,
        markers=True,
        title=f"{agg} {metric} Over Time"
    )

    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)


    # Insight
    st.markdown("### 💡 Insight")

    max_month = temp.loc[temp[metric].idxmax(), "YearMonth"]

    st.info(f"Peak performance in **{max_month}**")



# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption("Bivariate Analysis Dashboard | Developed by Eng. Mohamed")

import pandas as pd
import plotly.express as px
import streamlit as st
# Page Config
st.set_page_config(page_title="Online Sales Dashboard", layout="wide",page_icon='online-shop_164427.png')
#df = pd.read_csv("cleaned_dataset.csv")



# ================== Load Data ==================
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_dataset.csv")

df = load_data()



# ================= Title =================
st.title("📊 Univariate Analysis Dashboard")

st.markdown("""
Explore each feature individually to understand its behavior and distribution.
""")

st.divider()


# ================= Sidebar =================
st.sidebar.header("⚙️ Control Panel")

num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
exclude_cols = ["CustomerID", "InvoiceDate", "InvoiceNo"]

cat_cols = [
    col for col in df.select_dtypes(include="object").columns
    if col not in exclude_cols and df[col].nunique() < 50
]


analysis_type = st.sidebar.radio(
    "Select Analysis Type",
    ["Numerical", "Categorical"]
)


# ================= Numerical =================
if analysis_type == "Numerical":

    col = st.sidebar.selectbox("Select Column", num_cols)

    # ---------- Title ----------
    st.subheader(f"📈 Analysis: {col}")

    st.divider()


    # ---------- KPIs ----------
    c1, c2, c4, c5 = st.columns(4)

    c1.metric("Mean", f"{df[col].mean():,.2f}")
    c2.metric("Median", f"{df[col].median():,.2f}")
    c4.metric("Min", f"{df[col].min():,.2f}")
    c5.metric("Max", f"{df[col].max():,.2f}")


    st.divider()


    # ---------- Charts ----------
    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.histogram(
            df,
            x=col,
            nbins=30,
            title="Distribution"
        )

        st.plotly_chart(fig1, use_container_width=True)


    with col2:

        fig2 = px.box(
            df,
            y=col,
            title="Outliers"
        )

        st.plotly_chart(fig2, use_container_width=True)


    st.divider()


    # ---------- Insight ----------
    skew = df[col].skew()

    st.markdown("### 💡 Insight")

    if skew > 1:
        st.info("Right-skewed: Many small values, few large values.")

    elif skew < -1:
        st.info("Left-skewed: Many large values, few small values.")

    else:
        st.success("Approximately normal distribution.")



# ================= Categorical =================
else:

    col = st.sidebar.selectbox("Select Column", cat_cols)

    st.subheader(f"📊 Analysis: {col}")

    st.divider()


    counts = df[col].value_counts().reset_index()
    counts.columns = [col, "Count"]


    # ---------- KPIs ----------
    c1, c2, c3 = st.columns(3)

    c1.metric("Categories", counts.shape[0])
    c2.metric("Top Category", counts.iloc[0, 0])
    c3.metric("Top %", f"{(counts.iloc[0,1]/counts['Count'].sum()*100):.1f}%")


    st.divider()


    # ---------- Pie Columns ----------
    pie_cols = [
        "Customer_Type",
        "orderpriority",
        "shipmentprovider",
        "category",
        "paymentmethod",
        "returnstatus",
        "saleschannel"
    ]


    # ---------- Chart ----------
    if col in pie_cols:

        fig = px.pie(
            counts,
            names=col,
            values="Count",
            hole=0.4,
            title="Category Distribution"
        )

        fig.update_traces(textinfo="percent+label")

        st.plotly_chart(fig, use_container_width=True)


    else:

        fig = px.bar(
            counts,
            x=col,
            y="Count",
            text="Count",
            title="Category Frequency"
        )

        fig.update_traces(textposition="outside")

        st.plotly_chart(fig, use_container_width=True)


    st.divider()


    # ---------- Insight ----------
    st.markdown("### 💡 Insight")

    dominance = counts.iloc[0,1] / counts["Count"].sum() * 100

    if dominance > 51:
        st.warning("One category is dominant.")

    elif (dominance > 36) and (dominance <50) :
        st.info("Some categories are more frequent.")

    else:
        st.success("Categories are well balanced.")



# ================= Footer =================
st.markdown("---")
st.caption("Univariate Analysis | Developed by Eng. Mohamed")

import pandas as pd
import plotly.express as px
import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Online Sales Dashboard", layout="wide",page_icon='online-shop_164427.png')


# ================= CUSTOM STYLING =================
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    font-weight:600;
}
.metric-card {
    background-color:#111827;
    padding:15px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)
#

# ================= LOAD DATA =================
@st.cache_data
def load_data():

    df = pd.read_csv("cleaned_dataset.csv")

    num_cols = [
        "quantity", "unitprice", "shippingcost",
        "Gross_Sales", "Net_Revenue",
        "Total_Order_Value", "Shipping_Ratio",
        "discount"
    ]

    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "invoicedate" in df.columns:
        df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")

    return df


df = load_data()


# ================= PROFIT COLUMN =================
df["Profit"] = df["Net_Revenue"] - df["shippingcost"]


# ================= TITLE =================
st.title("🚀 Business Insights & Recommendations")
st.caption("From Data to Strategic Decisions")

st.divider()




# =====================================================
# 🎯 EXECUTIVE SUMMARY
# =====================================================

st.subheader("🎯 Executive Summary")

total_revenue = df["Net_Revenue"].sum()
total_profit = df["Profit"].sum()
return_rate = df["IsReturned"].mean()
top_category = df.groupby("category")["Net_Revenue"].sum().idxmax()
top_channel = df.groupby("saleschannel")["Net_Revenue"].sum().idxmax()

st.markdown(f"""
This business generated *{total_revenue:,.0f}   in total revenue with a total profit of  *{total_profit:,.0f}**.

- 📦 Top Revenue Category: **{top_category}**
- 🛒 Best Sales Channel: **{top_channel}**
- 🔄 Overall Return Rate: **{return_rate:.2%}**

📌 The company performance is stable with strong contribution from registered customers and balanced channel performance.
""")

st.divider()


# =====================================================
# 📊 KPI DASHBOARD
# =====================================================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🔄 Return Rate", f"{return_rate:.2%}")
col4.metric("📦 Total Orders", f"{len(df):,}")





# =====================================================
# ================= STRATEGIC QUESTIONS =================
# =====================================================

st.subheader("📌 Key Business Questions & Insights")


# =====================================================
# Q1 Do Discounts Increase Returns?
# =====================================================
with st.expander("1️⃣ Do higher discounts lead to more returned orders?"):

    data = df.groupby("IsReturned")["discount"].mean().reset_index()

    fig = px.bar(
        data,
        x="IsReturned",
        y="discount",
        text_auto=True,
        title="Average Discount by Return Status",
        labels={"IsReturned": "0 = NotReturned and 1 = Returned"},
        color='IsReturned'

    )

    st.plotly_chart(fig, use_container_width=True)

    diff = data.iloc[1]["discount"] - data.iloc[0]["discount"]

    st.metric("Discount Difference", f"{diff:.4f}")

    st.info("📌 Insight: Discounts do NOT significantly impact return rates.")


# =====================================================
# Q2 Highest Revenue Category
# =====================================================
with st.expander("2️⃣ Which category generates the highest revenue?"):

    data = df.groupby("category")["Net_Revenue"].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(
        data,
        x="category",
        y="Net_Revenue",
        text_auto=True,
        color="category",
        title="Total Net Revenue by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    top = data.iloc[0]["category"]

    st.success(f"🏆 Top Revenue Category: {top}")


# =====================================================
# Q3 Country with Highest Return Rate
# =====================================================
with st.expander("3️⃣ Which country has the highest return rate?"):

    data = df.groupby("country")["IsReturned"].mean().sort_values(ascending=False).reset_index()

    fig = px.bar(
        data.head(10),
        x="country",
        y="IsReturned",
        text_auto=".2%",
        title="Top 10 Countries by Return Rate"
    )

    st.plotly_chart(fig, use_container_width=True)

    worst = data.iloc[0]["country"]

    st.warning(f"⚠️ Highest Return Rate: {worst}")


# =====================================================
# Q4 Sales Channel Impact
# =====================================================
with st.expander("4️⃣ Does sales channel affect revenue?"):

    data = df.groupby("saleschannel")["Net_Revenue"].sum().reset_index()

    fig = px.bar(
        data,
        x="saleschannel",
        y="Net_Revenue",
        text_auto=True,
        color="saleschannel",
        title="Revenue by Sales Channel"
    )

    st.plotly_chart(fig, use_container_width=True)

    best = data.sort_values("Net_Revenue", ascending=False).iloc[0]["saleschannel"]

    st.success(f"🏆 Best Performing Channel: {best}")


# =====================================================
# Q5 Shipping Cost vs Revenue
# =====================================================
with st.expander("5️⃣ Is there a relationship between shipping cost and revenue?"):

    fig = px.scatter(
        df,
        x="shippingcost",
        y="Net_Revenue",
        trendline="ols",
        opacity=0.5,
        title="Shipping Cost vs Net Revenue"
    )

    st.plotly_chart(fig, use_container_width=True)

    corr = df["shippingcost"].corr(df["Net_Revenue"])

    st.metric("Correlation", f"{corr:.4f}")

    st.info("📌 Insight: Shipping cost has no meaningful impact on revenue.")


# =====================================================
# Q6 Customer Type Spending
# =====================================================
with st.expander("6️⃣ Which customer type spends more?"):

    data = df.groupby("Customer_Type")["Net_Revenue"].sum().reset_index()

    fig = px.pie(
        data,
        names="Customer_Type",
        values="Net_Revenue",
        title="Revenue Contribution by Customer Type"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("📌 Insight: Registered customers generate the majority of revenue.")


# =====================================================
# Q7 Seasonality Analysis
# =====================================================
with st.expander("7️⃣ Is there seasonality in sales?"):

    temp = df.dropna(subset=["invoicedate"]).copy()
    temp["Month"] = temp["invoicedate"].dt.month
    temp["Month_Name"] = temp["invoicedate"].dt.strftime("%b")

    data = temp.groupby(["Month","Month_Name"])["Net_Revenue"].sum().reset_index()
    data = data.sort_values("Month")

    fig = px.line(
        data,
        x="Month_Name",
        y="Net_Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("📌 Insight: Revenue fluctuates across months, indicating seasonality.")


# =====================================================
# Q8 Payment Method Revenue
# =====================================================
with st.expander("8️⃣ Which payment method generates the highest revenue?"):

    data = df.groupby("paymentmethod")["Net_Revenue"].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(
        data,
        x="paymentmethod",
        y="Net_Revenue",
        text_auto=True,
        title="Revenue by Payment Method"
    )

    st.plotly_chart(fig, use_container_width=True)

    top = data.iloc[0]["paymentmethod"]

    st.success(f"🏆 Top Payment Method: {top}")


# =====================================================
# Q9 Return Rate by Category
# =====================================================
with st.expander("9️⃣ Which category has the highest return rate?"):

    data = df.groupby("category")["IsReturned"].mean().sort_values(ascending=False).reset_index()

    fig = px.bar(
        data,
        x="category",
        y="IsReturned",
        text_auto=".2%",
        title="Return Rate by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    worst = data.iloc[0]["category"]

    st.warning(f"⚠️ Highest Return Category: {worst}")


# =====================================================
# Q10 Discount vs Profit
# =====================================================
with st.expander("🔟 How do discounts impact profit?"):

    fig = px.scatter(
        df,
        x="discount",
        y="Profit",
        trendline="ols",
        opacity=0.5,
        title="Discount vs Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

    corr = df["discount"].corr(df["Profit"])

    st.metric("Correlation", f"{corr:.4f}")

    st.info("📌 Insight: Excessive discounting may reduce profitability.")


# ================= FOOTER =================
st.markdown("---")
st.caption("Advanced Analytics & Strategy | Developed by Eng. Mohamed")

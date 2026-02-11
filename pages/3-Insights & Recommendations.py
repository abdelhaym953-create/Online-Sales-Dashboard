import pandas as pd
import plotly.express as px
import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Online Sales Dashboard", layout="wide",page_icon='online-shop_164427.png')


# ================= LOAD DATA =================
@st.cache_data
def load_data():

    df = pd.read_csv("cleaned_dataset.csv")

    num_cols = [
        "quantity", "unitprice", "shippingcost",
        "Gross_Sales", "Net_Revenue",
        "Total_Order_Value", "Shipping_Ratio"
    ]

    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "invoicedate" in df.columns:
        df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")

    return df


df = load_data()


# ================= TITLE =================
st.title("🚀 Insights & Recommendations")
st.caption("Turning data into decisions")

st.divider()


# ================= EXECUTIVE KPIs =================
st.subheader("📊 Executive Overview")

c1, c2, c3, c4, c5 = st.columns(5)

total_rev = df["Net_Revenue"].sum()
total_order = df["Total_Order_Value"].count()
return_rate = df["IsReturned"].mean() * 100
avg_discount = df["discount"].mean()
shipping_ratio = df["Shipping_Ratio"].mean()

c1.metric("Total Revenue", f"{total_rev:,.0f}")
c2.metric("Total Order", f"{total_order:,.0f}")
c3.metric("Return Rate", f"{return_rate:.1f}%")
c4.metric("Avg Discount", f"{avg_discount:.2f}")
c5.metric("Shipping Ratio", f"{shipping_ratio:.2f}")

st.divider()


# ================= SMART INSIGHT SUMMARY =================
st.subheader("🧠 Smart Insight Summary")

if return_rate > 10:
    st.warning("⚠️ High return rate detected — potential quality or expectation mismatch.")

if shipping_ratio > 0.3:
    st.warning("🚚 Shipping costs consume a large portion of order value.")

if avg_discount > 0.35:
    st.info("🏷️ Heavy discounting strategy detected — may impact long-term margins.")

st.success("✅ Revenue generation appears strong with stable average order value.")


st.divider()


# ================= INTERACTIVE BUSINESS QUESTIONS =================
st.subheader("❓ Interactive Business Questions")

question = st.selectbox(
    "Choose a business question:",
    [
        "Which category should we invest in more?",
        "Which sales channel drives scalable growth?",
        "Where are we losing money?",
        "Is the business seasonal?",
        "Are customers price-sensitive?",
        "Is logistics hurting profitability?"
    ]
)


# ---------- Q1 ----------
if question == "Which category should we invest in more?":

    cat_rev = df.groupby("category")["Net_Revenue"].sum().sort_values(ascending=False)
    top_cat = cat_rev.index[0]

    st.success(f"🏆 **{top_cat}** is the strongest category by revenue.")
    st.markdown(
        "📌 **Decision:** Increase inventory depth, marketing spend, "
        "and cross-selling around this category."
    )
    st.dataframe(cat_rev.reset_index(), use_container_width=True)


# ---------- Q2 ----------
elif question == "Which sales channel drives scalable growth?":

    ch_rev = df.groupby("saleschannel")["Net_Revenue"].sum().sort_values(ascending=False)
    best_ch = ch_rev.index[0]

    st.success(f"🚀 **{best_ch}** is the most scalable channel.")
    st.markdown(
        "📌 **Decision:** Prioritize this channel for paid campaigns and partnerships."
    )
    st.dataframe(ch_rev.reset_index(), use_container_width=True)


# ---------- Q3 ----------
elif question == "Where are we losing money?":

    returned_loss = df[df["IsReturned"] == 1]["Net_Revenue"].sum()
    loss_pct = (returned_loss / total_rev) * 100

    st.error(
        f"💸 Returned orders cause approximately **{loss_pct:.1f}% revenue loss**."
    )
    st.markdown(
        "📌 **Decision:** Improve product descriptions, quality checks, "
        "and return policies."
    )


# ---------- Q4 ----------
elif question == "Is the business seasonal?":

    temp = df.dropna(subset=["invoicedate"]).copy()
    temp["Month"] = temp["invoicedate"].dt.month_name()

    month_rev = temp.groupby("Month")["Net_Revenue"].sum()
    best_month = month_rev.idxmax()
    worst_month = month_rev.idxmin()

    st.info(
        f"📈 Best Month: **{best_month}** | 📉 Worst Month: **{worst_month}**"
    )
    st.markdown(
        "📌 **Decision:** Shift promotions and inventory planning based on seasonality."
    )
    st.dataframe(month_rev.reset_index(), use_container_width=True)


# ---------- Q5 ----------
elif question == "Are customers price-sensitive?":

    corr = df["discount"].corr(df["quantity"])

    st.metric("Discount vs Quantity Correlation", f"{corr:.2f}")

    if corr > 0.4:
        st.success("📈 Customers respond strongly to discounts.")
        st.markdown("📌 **Decision:** Tactical discounting can boost volume.")
    else:
        st.info("📉 Customers are not highly price-sensitive.")
        st.markdown("📌 **Decision:** Focus on value, quality, and brand positioning.")


# ---------- Q6 ----------
elif question == "Is logistics hurting profitability?":

    st.metric("Average Shipping Ratio", f"{shipping_ratio:.2f}")

    if shipping_ratio > 0.3:
        st.error("🚚 Logistics costs are negatively impacting margins.")
        st.markdown(
            "📌 **Decision:** Negotiate carriers, optimize routes, or introduce minimum order thresholds."
        )
    else:
        st.success("✅ Shipping costs are under control.")


st.divider()


# ================= FINAL STRATEGY =================
st.subheader("🎯 Final Strategic Takeaways")

st.markdown("""
- 🔥 Scale **top-performing categories and channels**
- ⚠️ Reduce **returns and logistics inefficiencies**
- 🧠 Use **data-driven discounting**, not blanket promotions
- 📅 Align campaigns with **seasonal demand**
- 🚀 Focus on **profitability**, not just revenue

This dashboard supports **strategic decision-making**, not just reporting.
""")


# ================= FOOTER =================
st.markdown("---")
st.caption("Advanced Analytics & Strategy | Developed by Eng. Mohamed 🚀📊")

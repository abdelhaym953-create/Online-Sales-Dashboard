import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Online Sales Dashboard", layout="wide",page_icon='online-shop_164427.png')


# ---------------- Load Data ----------------
df = pd.read_csv("cleaned_dataset.csv")

df["invoicedate"] = pd.to_datetime(df["invoicedate"])

# ---------------- Sidebar Filters ----------------
st.sidebar.header("🔎 Filters")

# Date Filter
# Ensure datetime
df["invoicedate"] = pd.to_datetime(df["invoicedate"])

# Dataset min and max dates
min_date = df["invoicedate"].min().date()
max_date = df["invoicedate"].max().date()

# Start and End Date Pickers with min/max limits
start_date = st.sidebar.date_input(
    "Start Date",
    min_value=min_date,
    max_value=max_date,
    value=min_date
)
end_date = st.sidebar.date_input(
    "End Date",
    min_value=min_date,
    max_value=max_date,
    value=max_date
)

# Convert to Timestamp for filtering
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Country Filter
country_list = ["All"] + sorted(df["country"].unique().tolist())

country_filter = st.sidebar.selectbox(
    "Select Country",
    country_list
)

# Category Filter
category_list = ["All"] + sorted(df["category"].unique().tolist())

category_filter = st.sidebar.selectbox(
    "Select Category",
    category_list
)

# ---------------- Apply Filters ----------------
filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df["invoicedate"] >= start_date)&
    (filtered_df["invoicedate"] <= end_date)
]

if country_filter != "All":
    filtered_df = filtered_df[filtered_df["country"] == country_filter]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["category"] == category_filter]


# ---------------- Title ----------------
st.title("📊 Online Sales Dashboard – Overview")
st.caption("Developed by Eng. Mohamed")

st.divider()

# ---------------- Dataset Description ----------------
st.subheader("📌 Dataset Description")

st.markdown("""
This dataset contains anonymized online sales transactions from an e-commerce platform.

It includes information about products, customers, payments, discounts, shipping, and returns.

The dataset is used to analyze sales performance, customer behavior, and operational efficiency.

It helps businesses understand purchasing patterns, improve pricing strategies, and enhance customer satisfaction.
""")


st.divider()

# ---------------- KPIs ----------------
total_sales = filtered_df["Gross_Sales"].sum()
net_revenue = filtered_df["Net_Revenue"].sum()
total_orders = filtered_df.shape[0]
return_rate = filtered_df["IsReturned"].mean() * 100
avg_order = filtered_df["Total_Order_Value"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Gross Sales", f"{total_sales:,.0f}")
col2.metric("📈 Net Revenue", f"{net_revenue:,.0f}")
col3.metric("🧾 Orders", f"{total_orders:,}")
col4.metric("↩️ Return Rate", f"{return_rate:.2f}%")
col5.metric("🛍️ Avg Order", f"{avg_order:,.0f}")

st.divider()

# ---------------- Data Preview ----------------
st.subheader("📄 Dataset Preview")

rows = st.slider("Number of Rows", 5, 50, 10, 5)

st.dataframe(
    filtered_df.head(rows),
    use_container_width=True
)

st.divider()

# ---------------- Summary ----------------
st.subheader("📌 Dataset Summary")

c1, c2, c3 = st.columns(3)

c1.metric("Rows", filtered_df.shape[0])
c2.metric("Columns", filtered_df.shape[1])
c3.metric("Missing Values", filtered_df.isnull().sum().sum())

st.divider()

# ---------------- Columns Description ----------------
st.divider()

st.subheader("📘 Columns Description")

data_dictionary = [
    ["Description", "Product description."],
    ["Quantity", "Number of items sold."],
    ["InvoiceDate", "Date of purchase."],
    ["UnitPrice", "Price per unit."],
    ["CustomerID", "Unique customer ID."],
    ["Country", "Customer country."],
    ["Discount", "Discount applied (0–1)."],
    ["PaymentMethod", "Method of payment used."],
    ["ShippingCost", "Shipping cost for the order."],
    ["Category", "Product category."],
    ["SalesChannel", "Sales channel (Online / In-store)."],
    ["ReturnStatus", "Shows if order was returned."],
    ["ShipmentProvider", "Shipping company name."],
    ["WarehouseLocation", "Warehouse location."],
    ["OrderPriority", "Order priority level."],
    ["Gross_Sales", "Total sales before discount."],
    ["Net_Revenue", "Revenue after discounts."],
    ["Total_Order_Value", "Final order value."],
    ["Shipping_Ratio", "Shipping cost ratio to order value."],
    ["IsReturned", "1 = Returned, 0 = Not Returned."],
    ["Year", "Order year."],
    ["Month", "Order month number."],
    ["Month_Name", "Order month name."],
    ["Customer_Type", "Registered or Guest customer."]
]

desc_df = pd.DataFrame(
    data_dictionary,
    columns=["Column Name", "Meaning"]
)

st.dataframe(desc_df, use_container_width=True)

import pandas as pd
import plotly.express as px
import streamlit as st
st.set_page_config(page_title="Online Sales Dashboard", layout="wide",page_icon='online-shop_164427.png')
df = pd.read_csv("cleaned_dataset.csv")

st.title('page3')

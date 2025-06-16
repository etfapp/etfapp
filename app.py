# app.py
import streamlit as st
import pandas as pd
from data_updater import update_etf_data

st.set_page_config(page_title="📊 ETF 總表", layout="wide")
st.title("📊 台股 ETF 總表 - Step 1 測試版")

@st.cache_data(ttl=3600)
def load_data():
    try:
        return pd.read_csv("etf_data.csv")
    except:
        return pd.DataFrame()

if st.button("🔁 手動更新資料"):
    try:
        update_etf_data()
        st.success("✅ 更新成功！請重新整理查看最新資料")
    except Exception as e:
        st.error(f"❌ 更新失敗：{e}")

df = load_data()
if df.empty:
    st.warning("⚠️ 尚無資料，請先按下『手動更新資料』")
else:
    st.dataframe(df, use_container_width=True)

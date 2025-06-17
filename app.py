
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ETF 助手", layout="wide")

st.title("📋 自選清單")

# 檔案路徑
watchlist_file = "watchlist.csv"
data_file = "etf_data.csv"

# 載入 ETF 資料
@st.cache_data
def load_etf_data():
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
        df["代碼"] = df["代碼"].astype(str)
        return df
    else:
        return pd.DataFrame()

# 載入自選清單
def load_watchlist():
    if os.path.exists(watchlist_file):
        df = pd.read_csv(watchlist_file)
        df["代碼"] = df["代碼"].astype(str)
        return df
    else:
        return pd.DataFrame(columns=["代碼"])

# 儲存自選清單
def save_watchlist(df):
    df.to_csv(watchlist_file, index=False)

etf_data = load_etf_data()
watchlist = load_watchlist()

# 搜尋與加入自選
code_input = st.text_input("🔍 輸入想加入的 ETF 代碼（如 0050）")
if st.button("➕ 加入自選") and code_input:
    if code_input not in watchlist["代碼"].values:
        watchlist = pd.concat([watchlist, pd.DataFrame({"代碼": [code_input]})], ignore_index=True)
        save_watchlist(watchlist)
        st.success(f"{code_input} 已加入自選清單")
    else:
        st.warning("該代碼已存在自選清單")

# 合併顯示
if not watchlist.empty and not etf_data.empty:
    merged = pd.merge(watchlist, etf_data, on="代碼", how="left")
    st.dataframe(merged)
else:
    st.write("⚠️ 尚無自選資料或 ETF 資料")

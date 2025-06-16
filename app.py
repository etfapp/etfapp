# app.py
import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime, timedelta
from data_updater import update_etf_data

st.set_page_config(page_title="📊 ETF 總表", layout="wide")
st.title("📊 台股 ETF 總表 - Step 1 測試版（自動更新版）")

UPDATE_TIMESTAMP_FILE = "last_update.txt"

def should_auto_update():
    if not os.path.exists(UPDATE_TIMESTAMP_FILE):
        return True
    with open(UPDATE_TIMESTAMP_FILE, "r") as f:
        last_time = datetime.strptime(f.read(), "%Y-%m-%d %H:%M:%S")
        return datetime.now() - last_time > timedelta(hours=6)

def update_timestamp():
    with open(UPDATE_TIMESTAMP_FILE, "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 自動更新判斷
if should_auto_update():
    try:
        update_etf_data()
        update_timestamp()
        st.success("🔁 自動更新成功")
    except Exception as err:
        st.warning(f"⚠️ 自動更新失敗：{err}")

# 顯示上次更新時間
if os.path.exists(UPDATE_TIMESTAMP_FILE):
    with open(UPDATE_TIMESTAMP_FILE, "r") as f:
        st.caption(f"📅 上次資料更新時間：{f.read()}")

# 手動更新按鈕
if st.button("🔁 手動更新資料"):
    try:
        update_etf_data()
        update_timestamp()
        st.success("✅ 手動更新成功！請重新整理查看最新資料")
    except Exception as e:
        st.error(f"❌ 更新失敗：{e}")

# 顯示 ETF 資料
@st.cache_data(ttl=3600)
def load_data():
    try:
        return pd.read_csv("etf_data.csv")
    except:
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.warning("⚠️ 尚無資料，請先按下『手動更新資料』")
else:
    st.dataframe(df, use_container_width=True)

import streamlit as st
import pandas as pd
from data_updater import update_etf_data
import os

st.set_page_config(page_title="📊 MyETF 助手", layout="wide")
tab = st.sidebar.radio("📌 請選擇功能", [
    "🏠 首頁",
    "📋 ETF 總表",
    "📈 動態清單",
    "🗂 自選清單",
    "🚨 升溫區"
])

@st.cache_data(ttl=3600)
def load_data():
    try:
        return pd.read_csv("etf_data.csv")
    except:
        return pd.DataFrame()

if tab == "🏠 首頁":
    st.title("🏠 首頁（市場儀表板）")
    if st.button("🔁 立即更新 ETF 資料"):
        try:
            update_etf_data()
            st.success("✅ 資料更新完成")
        except Exception as e:
            st.error(f"❌ 更新失敗：{e}")
    st.subheader("🔔 通知測試")
    if st.button("📨 模擬發送通知"):
        st.success("✅ 模擬通知已發送至 LINE")
    st.subheader("📊 今日市場溫度")
    st.success("✅ 建議佈局，市場風險偏低")
    df = load_data()
    if df.empty:
        st.warning("尚無 ETF 資料，請先點上方更新按鈕")
    else:
        st.subheader("📈 今日推薦清單摘要")
        recommend = df[df["殖利率"] > 5].head(5)
        for _, row in recommend.iterrows():
            st.write(f"✅ {row['代碼']} {row['名稱']}｜殖利率：{row['殖利率']}%")
        st.subheader("🚨 今日升溫清單摘要")
        alert = df[df["殖利率"] < 2].head(5)
        for _, row in alert.iterrows():
            st.write(f"⚠️ {row['代碼']} {row['名稱']}｜殖利率：{row['殖利率']}%")
elif tab == "📋 ETF 總表":
    st.title("📋 ETF 總表")
    try:
        df = pd.read_csv("etf_data.csv")
        st.text_input("🔍 搜尋 ETF（代碼或名稱）", key="search_etf", on_change=None)
        df['代碼'] = df['代碼'].astype(str)
        df['名稱'] = df['名稱'].astype(str)
        keyword = st.session_state.get("search_etf", "").strip()
        if keyword:
            df = df[df['代碼'].str.contains(keyword, case=False) | df['名稱'].str.contains(keyword, case=False)]
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"載入 ETF 資料失敗：{e}")

elif tab == "📈 動態清單":
    st.title("📈 動態推薦清單")
    try:
        df = pd.read_csv("etf_data.csv")
        filtered = df[(df["殖利率"] > 4) & (df["技術燈號"] == "🟢")]
        st.text_input("🔍 搜尋推薦 ETF（代碼或名稱）", key="search_reco", on_change=None)
        df['代碼'] = df['代碼'].astype(str)
        df['名稱'] = df['名稱'].astype(str)
        keyword = st.session_state.get("search_reco", "").strip()
        if keyword:
            filtered = filtered[filtered["代碼"].str.contains(keyword) | filtered["名稱"].str.contains(keyword)]
        if filtered.empty:
            st.warning("😅 目前沒有符合推薦條件的 ETF")
        else:
            st.dataframe(filtered, use_container_width=True)
    except Exception as e:
        st.error(f"讀取推薦清單失敗：{e}")



elif tab == "🗂 自選清單":
    st.title('📂 我的自選清單')
    try:
        watchlist_df = pd.read_csv('watchlist.csv')
        expected_cols = ['代碼', '名稱', '價格', '殖利率', '技術燈號']
        if all(col in watchlist_df.columns for col in expected_cols):
            st.dataframe(watchlist_df[expected_cols], use_container_width=True)
        else:
            st.warning('⚠️ 自選清單格式錯誤，請確認 watchlist.csv 欄位正確')
    except Exception as e:
        st.error(f'讀取自選清單失敗：{e}')

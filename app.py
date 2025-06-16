import streamlit as st
import pandas as pd
import datetime
from data_updater import update_etf_data

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

    # 手動更新按鈕
    if st.button("🔁 立即更新 ETF 資料"):
        try:
            update_etf_data()
            st.success("✅ 資料更新完成")
        except Exception as e:
            st.error(f"❌ 更新失敗：{e}")

    # 模擬市場判斷條件（之後可整合真實指標）
    st.subheader("📊 今日市場溫度")
    today = datetime.datetime.now().strftime("%Y/%m/%d")
    st.info(f"📅 今日日期：{today}")
    st.success("✅ 建議佈局，市場風險偏低")  # 模擬顯示（可接入 VIX、燈號等）

    # 載入資料後模擬摘要清單
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
        keyword = st.session_state.get("search_etf", "").strip()
        if keyword:
            df = df[df["代碼"].str.contains(keyword) | df["名稱"].str.contains(keyword)]
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"載入 ETF 資料失敗：{e}")
elif tab == "📈 動態清單":
    st.title("📈 動態清單")
    st.info("這裡將顯示由系統自動篩選的推薦 ETF 清單")

elif tab == "🗂 自選清單":
    st.title("🗂 我的自選清單")
    st.info("這裡將整合水位計算機與存股模擬器")

elif tab == "🚨 升溫區":
    st.title("🚨 升溫區")
    st.info("這裡會列出建議減碼／賣出的 ETF 並顯示原因")

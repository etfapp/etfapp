import streamlit as st
import pandas as pd
import os
from data_updater import update_etf_data

st.set_page_config(page_title="📊 MyETF助手 - 全新UI", layout="wide")
st.sidebar.title("📌 功能選單")
tab = st.sidebar.radio("請選擇功能", ["📈 推薦清單", "🗂 自選清單", "🔁 手動更新"])

@st.cache_data(ttl=3600)
def load_data():
    try:
        return pd.read_csv("etf_data.csv")
    except:
        return pd.DataFrame()

WATCHLIST_FILE = "watchlist.csv"
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        return pd.read_csv(WATCHLIST_FILE)
    else:
        return pd.DataFrame(columns=["代碼", "名稱"])

def save_watchlist(df):
    df.to_csv(WATCHLIST_FILE, index=False)

df = load_data()
watchlist = load_watchlist()

if tab == "📈 推薦清單":
    st.title("📈 推薦清單")
    if df.empty:
        st.warning("尚無資料，請先到『手動更新』分頁執行更新")
    else:
        recommend = df[df["殖利率"] > 5]
        if recommend.empty:
            st.info("目前無推薦標的（殖利率 > 5）")
        for i, row in recommend.iterrows():
            st.write(f"**{row['代碼']} {row['名稱']}**｜價格：{row['價格']}｜殖利率：{row['殖利率']}%｜{row['技術燈號']}")
            if st.button(f"➕ 加入自選 - {row['代碼']}", key=row['代碼']):
                if row['代碼'] not in watchlist['代碼'].values:
                    watchlist = pd.concat([watchlist, pd.DataFrame([row[["代碼", "名稱"]]])], ignore_index=True)
                    save_watchlist(watchlist)
                    st.success(f"{row['代碼']} 已加入自選清單！")

elif tab == "🗂 自選清單":
    st.title("🗂 我的自選清單")
    if watchlist.empty:
        st.info("尚未加入任何自選 ETF")
    else:
        st.dataframe(watchlist, use_container_width=True)
        code = st.text_input("輸入要移除的 ETF 代碼")
        if st.button("❌ 移除"):
            watchlist = watchlist[watchlist["代碼"] != code]
            save_watchlist(watchlist)
            st.success(f"{code} 已從自選清單移除")

elif tab == "🔁 手動更新":
    st.title("🔁 更新 ETF 資料")
    if st.button("📥 立即更新"):
        try:
            update_etf_data()
            st.success("✅ 資料更新成功！請切換到『推薦清單』或『自選清單』查看")
        except Exception as e:
            st.error(f"❌ 更新失敗：{e}")

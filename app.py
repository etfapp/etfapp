import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="📊 MyETF助手 Step 2", layout="wide")

@st.cache_data(ttl=3600)
def load_data():
    try:
        return pd.read_csv("etf_data.csv")
    except:
        return pd.DataFrame()

watchlist_file = "watchlist.csv"

def load_watchlist():
    if os.path.exists(watchlist_file):
        return pd.read_csv(watchlist_file)
    else:
        return pd.DataFrame(columns=["代碼", "名稱"])

def save_watchlist(df):
    df.to_csv(watchlist_file, index=False)

tab = st.sidebar.radio("📌 選擇功能", ["推薦清單", "自選清單"])

df = load_data()
watchlist = load_watchlist()

if tab == "推薦清單":
    st.title("🌟 推薦清單")
    if df.empty:
        st.warning("尚無 ETF 資料，請先更新。")
    else:
        st.caption("以下為系統根據殖利率推薦的 ETF（殖利率 > 5）")
        recommend = df[df["殖利率"] > 5]
        for i, row in recommend.iterrows():
            st.write(f"**{row['代碼']} - {row['名稱']}**｜殖利率：{row['殖利率']}%")
            if st.button(f"➕ 加入自選 - {row['代碼']}", key=f"add_{row['代碼']}"):
                if row['代碼'] not in watchlist['代碼'].values:
                    watchlist = pd.concat([watchlist, pd.DataFrame([row[["代碼", "名稱"]]])], ignore_index=True)
                    save_watchlist(watchlist)
                    st.success(f"{row['代碼']} 已加入自選清單！")

elif tab == "自選清單":
    st.title("🗂 自選清單")
    if watchlist.empty:
        st.info("尚未加入任何自選 ETF")
    else:
        st.dataframe(watchlist, use_container_width=True)
        remove_code = st.text_input("輸入想移除的 ETF 代碼")
        if st.button("❌ 移除"):
            watchlist = watchlist[watchlist["代碼"] != remove_code]
            save_watchlist(watchlist)
            st.success(f"{remove_code} 已從自選清單移除")

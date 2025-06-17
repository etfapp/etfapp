import streamlit as st
import pandas as pd
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

    # 🔧 修正欄位型別以支援 .str.contains()
    df['代碼'] = df['代碼'].astype(str)
    df['名稱'] = df['名稱'].astype(str)
        keyword = st.session_state.get("search_etf", "").strip()
        if keyword:
            df = df[df["代碼"].str.contains(keyword) | df["名稱"].str.contains(keyword)]
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"載入 ETF 資料失敗：{e}")

elif tab == "📈 動態清單":
    st.title("📈 動態推薦清單")
    try:
        df = pd.read_csv("etf_data.csv")
        filtered = df[(df["殖利率"] > 4) & (df["技術燈號"] == "🟢")]
        st.text_input("🔍 搜尋推薦 ETF（代碼或名稱）", key="search_reco", on_change=None)
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
    st.title("🗂 自選清單")
    try:
        df_all = pd.read_csv("etf_data.csv")
        df_watch = pd.read_csv("watchlist.csv")
        df_watch["代碼"] = df_watch["代碼"].astype(str)
        df_all["代碼"] = df_all["代碼"].astype(str)

        df_merged = pd.merge(df_watch, df_all, on="代碼", how="left")

        if df_merged.empty:
            st.warning("尚未加入任何自選 ETF")
        else:
            st.dataframe(df_merged[["代碼", "名稱_x", "價格", "殖利率", "位階分數"]].rename(columns={"名稱_x": "名稱"}), use_container_width=True)

            st.markdown("🔢 **股數計算（模擬）**")
            cash = st.number_input("💰 可投入金額（元）", min_value=0, step=1000)
            if cash > 0:
                df_valid = df_merged.dropna(subset=["價格"])
                df_valid["可買股數"] = (cash / df_valid["價格"]).astype(int)
                st.dataframe(df_valid[["代碼", "名稱_x", "價格", "可買股數"]].rename(columns={"名稱_x": "名稱"}), use_container_width=True)
    except Exception as e:
        st.error(f"❌ 載入自選清單失敗：{e}")

    st.title("🗂 我的自選清單")

    if "watchlist" not in st.session_state:
        st.session_state.watchlist = []

    new_etf = st.text_input("🔍 輸入想加入的 ETF 代碼（如 0050）")
    if st.button("➕ 加入自選"):
        if new_etf and new_etf not in st.session_state.watchlist:
            st.session_state.watchlist.append(new_etf)
            st.success(f"{new_etf} 已加入自選清單")

    st.subheader("📋 自選 ETF 清單")
    if st.session_state.watchlist:
        st.write(st.session_state.watchlist)
    else:
        st.info("尚未加入任何自選 ETF")

    st.subheader("💧 水位計算機")
    market_position = st.slider("目前市場位階建議佈局比例 (%)", 0, 100, 40)
    cash = st.number_input("請輸入目前手中現金 (元)", value=100000)
    deployable = int(cash * market_position / 100)
    st.write(f"💰 建議可佈局金額：約 {deployable:,} 元")

    st.subheader("📐 存股計算機")
    layout_count = st.number_input("預計佈局 ETF 檔數", min_value=1, value=2)
    st.write("👇 系統將幫你平均分配以下每檔投入金額與估算股數")
    if st.button("📊 計算佈局股數"):
        if not st.session_state.watchlist:
            st.warning("請先加入至少 1 檔自選 ETF")
        else:
            amount_per_etf = deployable / layout_count
            df = pd.read_csv("etf_data.csv")
            for etf in st.session_state.watchlist[:layout_count]:
                row = df[df["代碼"] == etf]
                if not row.empty:
                    price = float(row.iloc[0]["價格"])
                    shares = int(amount_per_etf // price)
                    st.write(f"✅ {etf} 建議佈局 {shares} 股（單價 {price} 元）")
                else:
                    st.write(f"⚠️ {etf} 資料缺失")

elif tab == "🚨 升溫區":
    st.title("🚨 升溫區（建議減碼／賣出）")

    try:
        df = pd.read_csv("etf_data.csv")

        # 假設進入升溫區條件：殖利率 < 2 或 技術燈號為 🔴
        heated = df[(df["殖利率"] < 2) | (df["技術燈號"] == "🔴")]

        st.text_input("🔍 搜尋升溫 ETF（代碼或名稱）", key="search_heat", on_change=None)
        keyword = st.session_state.get("search_heat", "").strip()
        if keyword:
            heated = heated[heated["代碼"].str.contains(keyword) | heated["名稱"].str.contains(keyword)]

        if heated.empty:
            st.success("✅ 目前沒有 ETF 進入升溫區")
        else:
            for _, row in heated.iterrows():
                st.write(f"⚠️ {row['代碼']} {row['名稱']}｜殖利率 {row['殖利率']}%，技術燈號：{row['技術燈號']}")
                reason = []
                if row["殖利率"] < 2:
                    reason.append("殖利率偏低")
                if row["技術燈號"] == "🔴":
                    reason.append("技術指標過熱")
                st.info("📌 升溫原因：" + "、".join(reason))
    except Exception as e:
        st.error(f"讀取升溫區資料失敗：{e}")

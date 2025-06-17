
import streamlit as st
import pandas as pd

st.set_page_config(page_title="MyETF助手", layout="wide")
st.title("📋 自選清單")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("etf_data.csv")
        if '代碼' in df.columns:
            df['代碼'] = df['代碼'].astype(str)
        return df
    except Exception as e:
        st.error(f"ETF 資料載入失敗：{e}")
        return pd.DataFrame()

def get_watchlist(df):
    watch_codes = ["0050", "00878"]  # 模擬自選
    watch_df = pd.DataFrame({"代碼": watch_codes})
    result = pd.merge(watch_df, df, on="代碼", how="left")
    return result

df = load_data()
watchlist = get_watchlist(df)

if not watchlist.empty:
    st.dataframe(watchlist)
else:
    st.warning("自選清單尚無資料")

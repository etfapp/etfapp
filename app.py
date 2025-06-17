
import pandas as pd
import streamlit as st

# 載入資料
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('etf_data.csv')
        if '代碼' in df.columns:
            try:
                df['代碼'] = df['代碼'].astype(str)
            except Exception as e:
                st.error(f"轉換代碼欄位為文字失敗：{e}")
        return df
    except Exception as e:
        st.error(f"載入 ETF 資料失敗：{e}")
        return pd.DataFrame()

st.title("ETF 資料總表測試")

df = load_data()
if not df.empty:
    st.dataframe(df)
else:
    st.warning("尚無資料可顯示")

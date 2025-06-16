# data_updater.py
import pandas as pd
import yfinance as yf

def update_etf_data():
    etfs = {
        "0050.TW": "元大台灣50",
        "00878.TW": "國泰永續高股息",
        "00929.TW": "復華台灣科技優息"
    }

    result = []
    for code, name in etfs.items():
        try:
            ticker = yf.Ticker(code)
            hist = ticker.history(period="5d")
            price = hist["Close"].iloc[-1] if not hist.empty else None
            info = ticker.info
            rsi = None
            dividend_yield = info.get("dividendYield", 0) or 0
            result.append({
                "代碼": code.replace(".TW", ""),
                "名稱": name,
                "價格": round(price, 2) if price else "N/A",
                "殖利率": round(dividend_yield * 100, 2),
                "RSI": rsi,
                "技術燈號": "🟢" if dividend_yield > 0.05 else "⚪️"
            })
        except:
            continue

    df = pd.DataFrame(result)
    df.to_csv("etf_data.csv", index=False)

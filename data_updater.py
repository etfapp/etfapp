import pandas as pd
import random

def update_etf_data():
    # 模擬更新資料，實際可接入 yfinance 或 TWSE 資料
    data = [
        {"代碼": "0050", "名稱": "元大台灣50", "價格": 140.5, "殖利率": round(random.uniform(1.5, 5.5), 2), "技術燈號": random.choice(["🟢", "⚪️", "🔴"])},
        {"代碼": "00878", "名稱": "國泰高股息", "價格": 18.3, "殖利率": round(random.uniform(1.5, 6.0), 2), "技術燈號": random.choice(["🟢", "⚪️", "🔴"])},
        {"代碼": "00929", "名稱": "復華科技優息", "價格": 21.7, "殖利率": round(random.uniform(1.0, 5.0), 2), "技術燈號": random.choice(["🟢", "⚪️", "🔴"])}
    ]
    df = pd.DataFrame(data)
    df.to_csv("etf_data.csv", index=False)

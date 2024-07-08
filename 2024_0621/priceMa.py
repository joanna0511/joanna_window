import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc

# 設置 matplotlib 使用微軟正黑體
plt.rcParams['font.family'] = 'Microsoft JhengHei'  # 設置字體為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 確保能正確顯示負號（例如負數）

# 定義股票代碼和資料時間範圍
stock_code = "2330.TW"
start_date = "2024-01-01"
end_date = "2024-06-21"

# 獲取台積電股票數據
tsmc = yf.download(stock_code, start=start_date, end=end_date)

# 計算移動平均線
tsmc['MA50'] = tsmc['Close'].rolling(window=50).mean()
tsmc['MA20'] = tsmc['Close'].rolling(window=20).mean()

# 轉換日期格式以繪製K棒圖
tsmc.reset_index(inplace=True)
tsmc['Date'] = tsmc['Date'].map(mdates.date2num)

# 繪製圖表
fig, ax = plt.subplots(figsize=(14, 7))

# 繪製K棒圖
ohlc = tsmc[['Date', 'Open', 'High', 'Low', 'Close']].values
candlestick_ohlc(ax, ohlc, colorup='red', colordown='green', width=0.6)

# 繪製移動平均線
ax.plot(tsmc['Date'], tsmc['MA20'], label='20日均線', color='orange') 
ax.plot(tsmc['Date'], tsmc['MA50'], label='50日均線', color='blue')

# 設置標題和標籤
ax.set_title('台積電股價及均價線')
ax.set_xlabel('日期') 
ax.set_ylabel('股價')
ax.legend()

# 格式化x軸日期
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# 調整子圖佈局以增加底部空間
plt.subplots_adjust(bottom=0.2)

plt.grid(True)
plt.show()

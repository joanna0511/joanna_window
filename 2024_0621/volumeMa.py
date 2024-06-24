import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 設置 matplotlib 使用微軟正黑體
plt.rcParams['font.family'] = 'Microsoft JhengHei'  # 設置字體為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 確保能正確顯示負號（例如負數）

# 定義股票代碼和資料時間範圍
stock_code = "2330.TW"
start_date = "2024-01-01"
end_date = "2024-06-21"

# 獲取台積電股票數據
tsmc = yf.download(stock_code, start=start_date, end=end_date)

# 計算成交量移動平均線
tsmc['Volume_MA5'] = tsmc['Volume'].rolling(window=5).mean()
tsmc['Volume_MA23'] = tsmc['Volume'].rolling(window=23).mean()

# 轉換日期格式以繪製圖表
tsmc.reset_index(inplace=True)
tsmc['Date'] = tsmc['Date'].map(mdates.date2num)

# 繪製圖表
fig, ax = plt.subplots(figsize=(14, 7))

# 繪製成交量柱狀圖
ax.bar(tsmc['Date'], tsmc['Volume'], label='成交量', color='gray', alpha=0.3)

# 繪製成交量移動平均線
ax.plot(tsmc['Date'], tsmc['Volume_MA5'], label='5日均線', color='blue')
ax.plot(tsmc['Date'], tsmc['Volume_MA23'], label='23日均線', color='orange')

# 設置標題和標籤
ax.set_title('台積電成交量及均量線')
ax.set_xlabel('日期')  
ax.set_ylabel('成交量')
ax.legend()

# 格式化x軸日期
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# 調整子圖佈局以增加底部空間
plt.subplots_adjust(bottom=0.2)

plt.grid(True)
plt.show()

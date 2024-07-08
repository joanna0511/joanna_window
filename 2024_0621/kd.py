import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# 設置 matplotlib 使用微軟正黑體
plt.rcParams['font.family'] = 'Microsoft JhengHei'  # 設置字體為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 確保能正確顯示負號（例如負數）

# 定義股票代碼和資料時間範圍
stock_code = "2330.TW"
start_date = "2024-01-01"
end_date = "2024-06-21"

# 獲取台積電股票數據
tsmc = yf.download(stock_code, start=start_date, end=end_date)

# 計算RSV (最近9天的最低價和最高價)
tsmc['min_9'] = tsmc['Low'].rolling(window=9).min()
tsmc['max_9'] = tsmc['High'].rolling(window=9).max()
tsmc['RSV'] = (tsmc['Close'] - tsmc['min_9']) / (tsmc['max_9'] - tsmc['min_9']) * 100

# 初始化K值和D值為浮點數
tsmc['K'] = 50.0  # 設置為浮點數
tsmc['D'] = 50.0  # 設置為浮點數

# 計算K值和D值，跳過NaN值的初始段
for i in range(9, len(tsmc)):
    tsmc.loc[tsmc.index[i], 'K'] = tsmc['K'].iloc[i-1] * 2/3 + tsmc['RSV'].iloc[i] * 1/3
    tsmc.loc[tsmc.index[i], 'D'] = tsmc['D'].iloc[i-1] * 2/3 + tsmc['K'].iloc[i] * 1/3

# 繪製K值和D值
plt.figure(figsize=(14, 7))
plt.plot(tsmc.index, tsmc['K'], label='K 值', color='blue')  
plt.plot(tsmc.index, tsmc['D'], label='D 值', color='red')  
plt.title('KD 指標')  
plt.xlabel('日期')  
plt.ylabel('數值')  
plt.legend()
plt.grid(True)
plt.show()

# 顯示最新的K值，格式化為小數點後兩位
latest_k_value = format(tsmc['K'].iloc[-1], ".2f")
#print("最新的K值為:", latest_k_value)  

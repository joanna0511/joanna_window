import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# 設置 matplotlib 使用微軟正黑體
plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False  # 確保能正確顯示負號（例如負數）

# 定義股票代碼和資料時間範圍import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# 設置 matplotlib 使用微軟正黑體
plt.rcParams['font.family'] = 'Microsoft JhengHei'
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
tsmc['K'] = 50.0
tsmc['D'] = 50.0

# 計算K值和D值
for i in range(9, len(tsmc)):
    tsmc.loc[tsmc.index[i], 'K'] = float(tsmc['K'].iloc[i-1] * 2/3 + tsmc['RSV'].iloc[i] * 1/3)
    tsmc.loc[tsmc.index[i], 'D'] = float(tsmc['D'].iloc[i-1] * 2/3 + tsmc['K'].iloc[i] * 1/3)

# 繪製K值和D值
plt.figure(figsize=(14, 8))  # 增加圖表高度以適應底部文字
plt.plot(tsmc.index, tsmc['K'], label='K值', color='blue')
plt.plot(tsmc.index, tsmc['D'], label='D值', color='red')
plt.title('KD指標')
plt.xlabel('日期')
plt.ylabel('值')
plt.legend()
plt.grid(True)

# 顯示最新的K值、D值
latest_k_value = format(tsmc['K'].iloc[-1], ".2f")
latest_d_value = format(tsmc['D'].iloc[-1], ".2f")
plt.figtext(0.1, -0.1, f'K值={latest_k_value}, D值={latest_d_value}', fontsize=24, color='black', ha='left', va='top')
plt.subplots_adjust(bottom=0.2)  # 調整底部空間以適應文字
plt.show()

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

# 計算K值和D值
for i in range(9, len(tsmc)):
    tsmc.loc[tsmc.index[i], 'K'] = float(tsmc['K'].iloc[i-1] * 2/3 + tsmc['RSV'].iloc[i] * 1/3)
    tsmc.loc[tsmc.index[i], 'D'] = float(tsmc['D'].iloc[i-1] * 2/3 + tsmc['K'].iloc[i] * 1/3)

# 繪製K值和D值
plt.figure(figsize=(14, 7))
plt.plot(tsmc.index, tsmc['K'], label='K值', color='blue')
plt.plot(tsmc.index, tsmc['D'], label='D值', color='red')
plt.title('KD指標')
plt.xlabel('日期')
plt.ylabel('值')
plt.legend()
plt.grid(True)

# 顯示最新的K值、D值
latest_k_value = format(tsmc['K'].iloc[-1], ".2f")
latest_d_value = format(tsmc['D'].iloc[-1], ".2f")
plt.figtext(0.1, -0.1, f'K值={latest_k_value}, D值={latest_d_value}', fontsize=24, color='black')
plt.show()

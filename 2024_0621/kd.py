import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

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

# 初始化K值和D值
tsmc['K'] = 50
tsmc['D'] = 50

# 計算K值和D值
for i in range(9, len(tsmc)):
    tsmc['K'].iloc[i] = tsmc['K'].iloc[i-1] * 2/3 + tsmc['RSV'].iloc[i] * 1/3
    tsmc['D'].iloc[i] = tsmc['D'].iloc[i-1] * 2/3 + tsmc['K'].iloc[i] * 1/3

# 計算狀態
def determine_status(k, d, k_prev, d_prev):
    if k >= d:
        if k_prev < d_prev:
            return '持續向上', 'red'
        elif k >= 80 and d > 80:
            return '高檔鈍化', 'red'
        else:
            return '向上', 'black'
    elif k < d:
        if k_prev > d_prev:
            return '持續向下', 'green'
        elif k < 20 and d <= 20:
            return '低檔鈍化', 'green'
        else:
            return '向下', 'black'
    else:
        return '轉折等待', 'blue'

# 繪製K值和D值
plt.figure(figsize=(14, 7))
plt.plot(tsmc.index, tsmc['K'], label='K value', color='blue')
plt.plot(tsmc.index, tsmc['D'], label='D value', color='red')
plt.title('KD Indicator')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid(True)

# 計算並顯示狀態
last_k = tsmc['K'].iloc[-1]
last_d = tsmc['D'].iloc[-1]
last_k_prev = tsmc['K'].iloc[-2]
last_d_prev = tsmc['D'].iloc[-2]
status, color = determine_status(last_k, last_d, last_k_prev, last_d_prev)
plt.figtext(0.1, -0.3, f'K值={last_k:.2f}, D值={last_d:.2f}, 狀態={status}', fontsize=24, color=color)
plt.show()

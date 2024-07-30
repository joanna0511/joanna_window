import yfinance as yf

# 定義要檢查的日期
dates_to_check = ['2024-06-29', '2024-07-13', '2024-07-21']
ticker = 'AAPL'  # 這裡可以使用任意有效的股票代碼

# 下載數據範圍內的股票數據
data = yf.download(ticker, start='2024-06-28', end='2024-07-22')

# 檢查這些日期是否有交易數據
available_dates = data.index.strftime('%Y-%m-%d').tolist()
missing_dates = [date for date in dates_to_check if date not in available_dates]

print("Missing dates (no trading data):", missing_dates)
print("Available dates:", available_dates)

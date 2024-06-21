import pandas_datareader.data as pdr
import yfinance as yf
yf.pdr_override()

# 定義股票代碼和資料時間範圍
stock_code = "2330.TW"
start_date = "2023-01-01"
end_date = "2023-06-21"

# 獲取台積電股票數據
data = pdr.get_data_yahoo(stock_code, start=start_date, end=end_date)

# 顯示前五行數據
print(data.head())

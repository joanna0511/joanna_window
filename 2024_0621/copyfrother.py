import pandas_datareader.data as pdr
import yfinance as yf
yf.pdr_override()

# 定義股票代碼和資料時間範圍
stock_code = "2330.TW"
start_date = "2024-01-01"
end_date = "2024-06-21"

# 獲取台積電股票數據
#data = pdr.get_data_yahoo(stock_code, start=start_date, end=end_date)

# 刪除 Adj Close 欄位
data = data.drop(columns=["Adj Close"])

# 顯示最後五行數據
print(data)

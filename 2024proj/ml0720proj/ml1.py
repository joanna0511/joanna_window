import yfinance as yf
import pandas as pd

# 設定股票代碼和時間範圍
tsmc_ticker = '2330.TW'
nvidia_ticker = 'NVDA'
start_date = '2013-07-19'
end_date = '2024-07-19'

# 下載台積電股價資料
tsmc_data = yf.download(tsmc_ticker, start=start_date, end=end_date)
# 將資料存成 CSV 檔案
tsmc_data.to_csv('tsmc10y.csv')

# 下載 NVIDIA 股價資料
nvidia_data = yf.download(nvidia_ticker, start=start_date, end=end_date)
# 將資料存成 CSV 檔案
nvidia_data.to_csv('nvidia10y.csv')

print("台積電和 NVIDIA 股價資料已經分別存成 tsmc10y.csv 和 nvidia10y.csv 檔案")

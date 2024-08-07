import yfinance as yf
import pandas as pd
import time  # 導入 time 模組

# 讀取csv檔
stock_list = pd.read_csv(r'D:\test1\stock_id.csv')  # 修改路徑格式
stock_list.columns = ['stock_id', 'name']
historical_data = pd.DataFrame()
for i in stock_list.index:
    # 抓取股票資料
    stock_id = stock_list.loc[i, 'stock_id'] + '.TW'
    data = yf.Ticker(stock_id)
    df = data.history(period="max")
    # 增加股票代號
    df['stock_id'] = stock_list.loc[i, 'stock_id']
    # 合併
    historical_data = pd.concat([historical_data, df])
    time.sleep(0.8)
historical_data.to_csv(r'D:\test1\historical_data.csv', index=False)  # 修改路徑格式

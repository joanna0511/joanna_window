import pandas as pd
import statsmodels.api as sm
import yfinance as yf

class StockPriceFetcher:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_data(self, start_date, end_date):
        self.data = yf.download(self.ticker, start=start_date, end=end_date)

    def save_to_csv(self, filename):
        self.data.to_csv(filename)
        print(f"{self.ticker} 股價資料已儲存至 {filename}")

def main():
    # 定義要取得股價的公司
    tickers = {"TSMC": "2330.TW", "NVIDIA": "NVDA"}

    # 取得近5年的日期範圍
    end_date = pd.to_datetime("today").date()
    start_date = end_date - pd.DateOffset(years=5)

    # 下載並儲存台積電和NVIDIA的股價資料
    for company, ticker in tickers.items():
        fetcher = StockPriceFetcher(ticker)
        fetcher.fetch_data(start_date, end_date)
        fetcher.save_to_csv(f"{company}_5years.csv")

if __name__ == "__main__":
    main()

# 讀取CSV檔案
nvidia_data = pd.read_csv('NVIDIA_5years.csv')
tsmc_data = pd.read_csv('TSMC_5years.csv')

# 提取日期和收盤價
nvidia_data['Date'] = pd.to_datetime(nvidia_data['Date'])
tsmc_data['Date'] = pd.to_datetime(tsmc_data['Date'])

nvidia_close = nvidia_data[['Date', 'Close']]
tsmc_close = tsmc_data[['Date', 'Close']]

# 合併資料
merged_data = pd.merge(nvidia_close, tsmc_close, on='Date', suffixes=('_NVIDIA', '_TSMC')).dropna()

# 回歸分析
X = merged_data['Close_NVIDIA'].values.reshape(-1, 1)
y = merged_data['Close_TSMC'].values

# 添加常數項以適應 statsmodels 的需求
X_sm = sm.add_constant(X)

# 建立 OLS 模型
model = sm.OLS(y, X_sm)
results = model.fit()

# 取得詳細的回歸分析結果
regression_summary = results.summary()
print(regression_summary)

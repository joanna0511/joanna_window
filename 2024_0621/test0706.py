import yfinance as yf
import pandas as pd

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

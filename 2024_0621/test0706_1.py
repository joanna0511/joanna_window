import yfinance as yf
import datetime

def fetch_stock_data(symbol, start_date):
    # Fetch the stock data
    stock_data = yf.download(symbol, start=start_date)
    return stock_data

def save_to_csv(data, filename):
    # Save the DataFrame to a CSV file
    data.to_csv(filename)

if __name__ == "__main__":
    # Calculate the date 5 years ago from today
    five_years_ago = datetime.datetime.now() - datetime.timedelta(days=5*365)

    # Symbols for NVIDIA and TSMC
    symbols = {'NVDA': 'NVDA', 'TSM': 'TSM'}

    for symbol in symbols:
        print(f"Fetching data for {symbol}")
        data = fetch_stock_data(symbols[symbol], five_years_ago.strftime('%Y-%m-%d'))
        filename = f"{symbol}_stock_data.csv"
        save_to_csv(data, filename)
        print(f"Data for {symbol} saved to {filename}")

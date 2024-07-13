import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def plot_kd_chart(self, data):
    low_min = data['Low'].rolling(window=9).min()
    high_max = data['High'].rolling(window=9).max()
    data['K'] = (data['Close'] - low_min) / (high_max - low_min) * 100
    data['D'] = data['K'].rolling(window=3).mean()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data.index, data['K'], label='K')
    ax.plot(data.index, data['D'], label='D')
    ax.set_title('KD指標圖')
    ax.legend()
    self.display_chart(fig)

def plot_ma_chart(self, data):
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.plot(data.index, data['MA20'], label='20-Day MA')
    ax.plot(data.index, data['MA50'], label='50-Day MA')
    ax.set_title('均價指標圖')
    ax.legend()
    self.display_chart(fig)

def plot_volume_chart(self, data):
    data.reset_index(inplace=True)
    data['DateInt'] = data.index
    data['VMA5'] = data['Volume'].rolling(window=5).mean()
    data['VMA23'] = data['Volume'].rolling(window=23).mean()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(data['DateInt'], data['Volume'], label='Volume', color='lightblue')
    ax.plot(data['DateInt'], data['VMA5'], label='5-Day Volume MA', color='orange')
    ax.plot(data['DateInt'], data['VMA23'], label='23-Day Volume MA', color='green')
    ax.set_title('均量指標圖')
    ax.legend()
    locator = DayLocator(interval=30)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    self.display_chart(fig)

def plot_normal_distribution(self, data):
    returns = data['Close'].pct_change().dropna()
    mu = returns.mean()
    sigma = returns.std()
    fig, ax = plt.subplots(figsize=(8, 4))
    count, bins, ignored = ax.hist(returns, bins=30, density=True, alpha=0.6, color='g')
    ax.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
    ax.set_title('常態分佈圖')
    self.display_chart(fig)

def plot_boxplot(self, data):
    returns = data['Close'].pct_change().dropna()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.boxplot(returns, vert=False)
    ax.set_title('盒鬚圖')
    ax.set_xlabel('日回報率')
    self.display_chart(fig)

def plot_moving_average_cross(self, data):
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.plot(data.index, data['MA50'], label='50-Day MA')
    ax.plot(data.index, data['MA200'], label='200-Day MA')

    golden_cross = (data['MA50'] > data['MA200']) & (data['MA50'].shift(1) <= data['MA200'].shift(1))
    death_cross = (data['MA50'] < data['MA200']) & (data['MA50'].shift(1) >= data['MA200'].shift(1))

    ax.plot(data.index[golden_cross], data['Close'][golden_cross], '^', markersize=10, color='g', lw=0, label='Golden Cross')
    ax.plot(data.index[death_cross], data['Close'][death_cross], 'v', markersize=10, color='r', lw=0, label='Death Cross')
    
    ax.set_title('移動平均線交叉')
    ax.legend()
    self.display_chart(fig)

def plot_bollinger_bands(self, data):
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['STD'] = data['Close'].rolling(window=20).std()
    data['Upper'] = data['MA20'] + (data['STD'] * 2)
    data['Lower'] = data['MA20'] - (data['STD'] * 2)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.plot(data.index, data['MA20'], label='20-Day MA')
    ax.plot(data.index, data['Upper'], label='Upper Band')
    ax.plot(data.index, data['Lower'], label='Lower Band')

    ax.fill_between(data.index, data['Lower'], data['Upper'], color='grey', alpha=0.3)

    ax.set_title('布林帶')
    ax.legend()
    self.display_chart(fig)

def plot_rsi(self, data):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data.index, data['RSI'], label='RSI')
    ax.axhline(70, color='r', linestyle='--')
    ax.axhline(30, color='g', linestyle='--')
    ax.set_title('相對強弱指數（RSI）')
    ax.legend()
    self.display_chart(fig)

def plot_macd(self, data):
    data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data.index, data['MACD'], label='MACD')
    ax.plot(data.index, data['Signal'], label='Signal')
    ax.set_title('移動平均收斂背馳（MACD）')
    ax.legend()
    self.display_chart(fig)

def plot_heatmap(self, data):
    data['Year'] = data.index.year
    data['Month'] = data.index.month
    pivot_table = data.pivot_table(values='Close', index='Month', columns='Year', aggfunc='mean')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title('股價熱力圖')
    self.display_chart(fig)

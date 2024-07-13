import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter, DayLocator

def plot_kd_chart(self, data):
    low_min = data['Low'].rolling(window=9).min()
    high_max = data['High'].rolling(window=9).max()
    data['K'] = (data['Close'] - low_min) / (high_max - low_min) * 100
    data['D'] = data['K'].rolling(window=3).mean()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data.index, data['K'], label='K')
    ax.plot(data.index, data['D'], label='D')
    ax.axhline(50, color='gray', linestyle='--', linewidth=1, label='K=50')
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

def plot_heatmap(self, data):
    data['Year'] = data.index.year
    data['Month'] = data.index.month
    pivot_table = data.pivot_table(values='Close', index='Month', columns='Year', aggfunc='mean')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title('股價熱力圖')
    self.display_chart(fig)

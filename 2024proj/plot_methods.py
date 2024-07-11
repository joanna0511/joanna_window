import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator

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
# 其他方法類似...

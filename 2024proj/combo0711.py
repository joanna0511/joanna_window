import tkinter as tk
from tkinter import ttk
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.dates import DateFormatter, DayLocator

# 設置 matplotlib 使用支持中文的字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決座標軸負號顯示問題

# 創建主窗口
root = tk.Tk()
root.title("股價整合系統")

# 定義股票代號對應表
stock_dict = {
    "TSMC": "TSM",
    "NVIDIA": "NVDA",
    "APPLE": "AAPL"
}

# 定義圖形選項
chart_options = ["KD指標圖", "均價指標圖", "均量指標圖", "常態分佈圖"]

# 創建下拉選單和按鈕
stock_label = tk.Label(root, text="選擇股票:")
stock_label.grid(row=0, column=0)
stock_var = tk.StringVar(value="TSMC")  # 設置預設值
stock_menu = ttk.Combobox(root, textvariable=stock_var, values=list(stock_dict.keys()))
stock_menu.grid(row=0, column=1)

chart_label = tk.Label(root, text="選擇圖形:")
chart_label.grid(row=1, column=0)
chart_var = tk.StringVar(value="KD指標圖")  # 設置預設值
chart_menu = ttk.Combobox(root, textvariable=chart_var, values=chart_options)
chart_menu.grid(row=1, column=1)

def plot_chart():
    stock = stock_var.get()
    chart_type = chart_var.get()
    if stock and chart_type:
        ticker = stock_dict[stock]
        try:
            stock_data = yf.download(ticker, period="1y")
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"無法獲取股票數據: {e}")
            return

        if chart_type == "KD指標圖":
            plot_kd_chart(stock_data)
        elif chart_type == "均價指標圖":
            plot_ma_chart(stock_data)
        elif chart_type == "均量指標圖":
            plot_volume_chart(stock_data)
        elif chart_type == "常態分佈圖":
            plot_normal_distribution(stock_data)

def plot_kd_chart(data):
    # 計算KD指標
    low_min = data['Low'].rolling(window=9).min()
    high_max = data['High'].rolling(window=9).max()
    data['K'] = (data['Close'] - low_min) / (high_max - low_min) * 100
    data['D'] = data['K'].rolling(window=3).mean()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data.index, data['K'], label='K')
    ax.plot(data.index, data['D'], label='D')
    ax.set_title('KD指標圖')
    ax.legend()
    display_chart(fig)

def plot_ma_chart(data):
    # 繪製均價指標圖
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.plot(data.index, data['MA20'], label='20-Day MA')
    ax.plot(data.index, data['MA50'], label='50-Day MA')
    ax.set_title('均價指標圖')
    ax.legend()
    display_chart(fig)

def plot_volume_chart(data):
    # 將日期索引轉換為整數索引
    data.reset_index(inplace=True)  # 重設索引
    data['DateInt'] = data.index  # 創建一個整數索引列

    # 繪製均量指標圖
    data['VMA5'] = data['Volume'].rolling(window=5).mean()
    data['VMA23'] = data['Volume'].rolling(window=23).mean()

    fig, ax = plt.subplots(figsize=(8, 4))
    # 使用整數索引繪製長條圖，確保長條間隔一致
    ax.bar(data['DateInt'], data['Volume'], label='Volume', color='lightblue')  # 更改了這裡
    ax.plot(data['DateInt'], data['VMA5'], label='5-Day Volume MA', color='orange')  # 更改了這裡
    ax.plot(data['DateInt'], data['VMA23'], label='23-Day Volume MA', color='green')  # 更改了這裡
    ax.set_title('均量指標圖')
    ax.legend()
    locator = DayLocator(interval=30)  # 每 30 天顯示一次
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()  # 自動旋轉日期標籤

    # 修正x軸的標籤以顯示日期
    ax.set_xticks(data['DateInt'][::30])  # 每30個數據點顯示一次
    ax.set_xticklabels([pd.to_datetime(date).strftime('%Y-%m-%d') for date in data['Date'][::30]], rotation=45)  # 格式化日期

    display_chart(fig)


def plot_normal_distribution(data):
    # 繪製常態分佈圖
    returns = data['Close'].pct_change().dropna()
    mu = returns.mean()
    sigma = returns.std()

    fig, ax = plt.subplots(figsize=(8, 4))
    count, bins, ignored = ax.hist(returns, bins=30, density=True, alpha=0.6, color='g')
    ax.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
    ax.set_title('常態分佈圖')
    display_chart(fig)

def display_chart(fig):
    for widget in root.grid_slaves(row=0, column=2):
        widget.grid_forget()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, rowspan=6)

# 創建執行按鈕
plot_button = tk.Button(root, text="執行", command=plot_chart)
plot_button.grid(row=2, column=0, columnspan=2)

# 預設顯示 TSMC 的 KD 指標圖
plot_chart()

# 運行主循環
root.mainloop()

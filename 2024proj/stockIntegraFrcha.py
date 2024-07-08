import tkinter as tk
from tkinter import ttk
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# 設置 matplotlib 使用支持中文的字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決座標軸負號顯示問題

# 創建主窗口並設置大小
root = tk.Tk()
root.title("股價整合系統")

# 獲取螢幕大小
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 設置窗口大小為螢幕大小減去寬度150像素，高度適當減少
window_width = screen_width - 150
window_height = int(screen_height * 0.8)  # 高度減少20%
root.geometry(f"{window_width}x{window_height}")

# 定義股票代號對應表
stock_dict = {
    "TSMC": "TSM",
    "NVIDIA": "NVDA",
    "APPLE": "AAPL"
}

# 定義圖形選項
chart_options = ["KD指標圖", "均價指標圖", "均量指標圖", "常態分佈圖"]

# 創建下拉選單和按鈕
stock_label = tk.Label(root, text="選擇股票:", font=("Microsoft JhengHei", 14))
stock_label.grid(row=0, column=0, padx=10, pady=10)
stock_var = tk.StringVar(value="TSMC")  # 設置預設值
stock_menu = ttk.Combobox(root, textvariable=stock_var, values=list(stock_dict.keys()), font=("Microsoft JhengHei", 14))
stock_menu.grid(row=0, column=1, padx=10, pady=10)

chart_label = tk.Label(root, text="選擇圖形:", font=("Microsoft JhengHei", 14))
chart_label.grid(row=1, column=0, padx=10, pady=10)
chart_var = tk.StringVar(value="KD指標圖")  # 設置預設值
chart_menu = ttk.Combobox(root, textvariable=chart_var, values=chart_options, font=("Microsoft JhengHei", 14))
chart_menu.grid(row=1, column=1, padx=10, pady=10)

def plot_chart():
    stock = stock_var.get()
    chart_type = chart_var.get()
    if stock and chart_type:
        ticker = stock_dict[stock]
        stock_data = yf.download(ticker, period="1y")
        stock_data = stock_data[stock_data['Volume'] != 0]  # 過濾掉Volume為0的數據

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
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['K'], label='K')
    ax.plot(data.index, data['D'], label='D')
    ax.set_title('KD指標圖', fontsize=16)
    ax.legend()
    display_chart(fig)

def plot_ma_chart(data):
    # 繪製均價指標圖
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.plot(data.index, data['MA20'], label='20-Day MA')
    ax.plot(data.index, data['MA50'], label='50-Day MA')
    ax.set_title('均價指標圖', fontsize=16)
    ax.legend()
    display_chart(fig)

def plot_volume_chart(data):
    # 繪製均量指標圖
    data['VMA5'] = data['Volume'].rolling(window=5).mean()
    data['VMA23'] = data['Volume'].rolling(window=23).mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(data.index, data['Volume'], label='Volume', color='gray', alpha=0.3)
    ax.plot(data.index, data['VMA5'], label='5-Day VMA', color='blue')
    ax.plot(data.index, data['VMA23'], label='23-Day VMA', color='red')
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Volume', fontsize=14)
    ax.set_title('均量指標圖', fontsize=16)
    ax.legend()
    
    # 設定工具列
    fig.autofmt_xdate()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
    plt.grid(True)
    
    display_chart(fig, toolbar=True)

def plot_normal_distribution(data):
    # 繪製常態分佈圖
    returns = data['Close'].pct_change().dropna()
    mu = returns.mean()
    sigma = returns.std()

    fig, ax = plt.subplots(figsize=(12, 6))
    count, bins, ignored = ax.hist(returns, bins=30, density=True, alpha=0.6, color='g')
    ax.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
    ax.set_title('常態分佈圖', fontsize=16)
    display_chart(fig)

def display_chart(fig, toolbar=False):
    for widget in root.grid_slaves(row=0, column=2):
        widget.grid_forget()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, rowspan=6)
    if toolbar:
        toolbar_frame = tk.Frame(root)
        toolbar_frame.grid(row=6, column=2, padx=10, pady=10)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=6)

# 創建執行按鈕
plot_button = tk.Button(root, text="執行", command=plot_chart, font=("Microsoft JhengHei", 14))
plot_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# 預設顯示 TSMC 的 KD 指標圖
plot_chart()

# 運行主循環
root.mainloop()

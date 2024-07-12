import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.dates import DateFormatter, DayLocator

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("股價整合系統")
        
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        self.stock_dict = {
            "TSMC": "TSM",
            "NVIDIA": "NVDA",
            "APPLE": "AAPL"
        }
        self.chart_options = ["KD指標圖", "均價指標圖", "均量指標圖", "常態分佈圖"]
        
        self.create_widgets()
        self.plot_chart(initial=True)  # 調用繪圖功能以預設顯示

    def create_widgets(self):
        stock_label = tk.Label(self.root, text="選擇股票:")
        stock_label.grid(row=0, column=0)
        self.stock_var = tk.StringVar(value="TSMC")
        stock_menu = ttk.Combobox(self.root, textvariable=self.stock_var, values=list(self.stock_dict.keys()))
        stock_menu.grid(row=0, column=1)
        
        chart_label = tk.Label(self.root, text="選擇圖形:")
        chart_label.grid(row=1, column=0)
        self.chart_var = tk.StringVar(value="KD指標圖")
        chart_menu = ttk.Combobox(self.root, textvariable=self.chart_var, values=self.chart_options)
        chart_menu.grid(row=1, column=1)
        
        plot_button = tk.Button(self.root, text="執行", command=self.plot_chart)
        plot_button.grid(row=2, column=0, columnspan=2)

    def plot_chart(self, initial=False):
        stock = self.stock_var.get() if not initial else "TSMC"
        chart_type = self.chart_var.get() if not initial else "KD指標圖"
        ticker = self.stock_dict.get(stock, None)
        if ticker:
            try:
                stock_data = yf.download(ticker, period="1y")
            except Exception as e:
                messagebox.showerror("錯誤", f"無法獲取股票數據: {e}")
                return
            
            if chart_type == "KD指標圖":
                self.plot_kd_chart(stock_data)
            elif chart_type == "均價指標圖":
                self.plot_ma_chart(stock_data)
            elif chart_type == "均量指標圖":
                self.plot_volume_chart(stock_data)
            elif chart_type == "常態分佈圖":
                self.plot_normal_distribution(stock_data)

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
    # 其他繪圖方法的實現...

    def display_chart(self, fig):
        for widget in self.root.grid_slaves(row=0, column=2):
            widget.grid_forget()
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=6)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()

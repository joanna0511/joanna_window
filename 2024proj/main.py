import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from plot_methods import plot_kd_chart, plot_ma_chart, plot_volume_chart, plot_normal_distribution, plot_boxplot, plot_moving_average_cross, plot_bollinger_bands, plot_rsi, plot_macd, plot_heatmap
from datetime import datetime, timedelta

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("股價整合系統")
        
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體
        plt.rcParams['axes.unicode_minus'] = False  # 解決座標軸負號顯示問題
        
        self.stock_dict = {
            "TSMC(ADR)": "TSM",
            "TSMC(台股)": "2330.TW",
            "NVIDIA": "NVDA",
            "APPLE": "AAPL"
        }
        self.chart_options = ["KD指標圖", "均價指標圖", "均量指標圖", "常態分佈圖", "盒鬚圖", "移動平均線交叉", "布林帶", "RSI", "MACD", "熱力圖"]  # 添加新選項
        self.time_options = ["1月", "3月", "6月", "1年", "2年"]  # 添加時間範圍選項
        self.create_widgets()
        self.plot_chart(initial=True)  # 調用繪圖功能以預設顯示

    def create_widgets(self):
        stock_label = tk.Label(self.root, text="選擇股票:")
        stock_label.grid(row=0, column=0)
        self.stock_var = tk.StringVar(value="TSMC(ADR)")
        stock_menu = ttk.Combobox(self.root, textvariable=self.stock_var, values=list(self.stock_dict.keys()))
        stock_menu.grid(row=0, column=1)

        time_label = tk.Label(self.root, text="選擇時間範圍:")
        time_label.grid(row=1, column=0)
        self.time_var = tk.StringVar(value="1年")
        time_menu = ttk.Combobox(self.root, textvariable=self.time_var, values=self.time_options)
        time_menu.grid(row=1, column=1)
        
        chart_label = tk.Label(self.root, text="選擇圖形:")
        chart_label.grid(row=2, column=0)
        self.chart_var = tk.StringVar(value="KD指標圖")
        chart_menu = ttk.Combobox(self.root, textvariable=self.chart_var, values=self.chart_options)
        chart_menu.grid(row=2, column=1)
        
        plot_button = tk.Button(self.root, text="執行", command=self.plot_chart)
        plot_button.grid(row=3, column=0, columnspan=2)

    def get_period(self, time_option):
        if time_option == "1月":
            return 30
        elif time_option == "3月":
            return 90
        elif time_option == "6月":
            return 180
        elif time_option == "1年":
            return 365
        elif time_option == "2年":
            return 730

    def plot_chart(self, initial=False):
        stock = self.stock_var.get() if not initial else "TSMC(ADR)"
        chart_type = self.chart_var.get() if not initial else "KD指標圖"
        time_option = self.time_var.get() if not initial else "1年"
        ticker = self.stock_dict.get(stock, None)
        if ticker:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.get_period(time_option))  # 根據用戶選擇的時間範圍設置日期
            try:
                stock_data = yf.download(ticker, start=start_date, end=end_date)
            except Exception as e:
                messagebox.showerror("錯誤", f"無法獲取股票數據: {e}")
                return
            
            if chart_type == "KD指標圖":
                plot_kd_chart(self, stock_data)
            elif chart_type == "均價指標圖":
                plot_ma_chart(self, stock_data)
            elif chart_type == "均量指標圖":
                plot_volume_chart(self, stock_data)
            elif chart_type == "常態分佈圖":
                plot_normal_distribution(self, stock_data)
            elif chart_type == "盒鬚圖":
                plot_boxplot(self, stock_data)
            elif chart_type == "移動平均線交叉":
                plot_moving_average_cross(self, stock_data)
            elif chart_type == "布林帶":
                plot_bollinger_bands(self, stock_data)
            elif chart_type == "RSI":
                plot_rsi(self, stock_data)
            elif chart_type == "MACD":
                plot_macd(self, stock_data)
            elif chart_type == "熱力圖":
                plot_heatmap(self, stock_data)

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

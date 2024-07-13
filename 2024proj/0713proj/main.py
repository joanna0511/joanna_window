import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from plot_methods import plot_kd_chart, plot_ma_chart, plot_volume_chart, plot_normal_distribution, plot_boxplot, plot_rsi, plot_heatmap
from datetime import datetime, timedelta

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("股價整合系統")
        
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        self.stock_dict = {
            "TSMC(ADR)": "TSM",
            "TSMC(台股)": "2330.TW",
            "NVIDIA": "NVDA",
            "APPLE": "AAPL"
        }
        
        self.chart_options = ["KD指標圖", "均價指標圖", "均量指標圖", "RSI", "常態分佈圖", "盒鬚圖", "熱力圖"]
        self.time_options = ["1月", "3月", "6月", "1年", "2年"]
        
        self.create_widgets()
        self.plot_chart(initial=True)

    def create_widgets(self):
        stock_label = tk.Label(self.root, text="選擇股票:")
        stock_label.grid(row=0, column=0)
        self.stock_var = tk.StringVar(value="TSMC(ADR)")
        stock_menu = ttk.Combobox(self.root, textvariable=self.stock_var, values=list(self.stock_dict.keys()), state="readonly")
        stock_menu.grid(row=0, column=1)

        time_label = tk.Label(self.root, text="選擇時間範圍:")
        time_label.grid(row=1, column=0)
        self.time_var = tk.StringVar(value="1年")
        time_menu = ttk.Combobox(self.root, textvariable=self.time_var, values=self.time_options, state="readonly")
        time_menu.grid(row=1, column=1)

        chart_label = tk.Label(self.root, text="選擇圖形:")
        chart_label.grid(row=2, column=0)
        self.chart_var = tk.StringVar(value="KD指標圖")
        chart_menu = ttk.Combobox(self.root, textvariable=self.chart_var, values=self.chart_options, state="readonly")
        chart_menu.grid(row=2, column=1)

        execute_button = tk.Button(self.root, text="執行", command=self.plot_chart)
        execute_button.grid(row=3, column=1, sticky=tk.W+tk.E)



    def plot_chart(self, initial=False):
        stock = self.stock_var.get() if not initial else "TSMC(ADR)"
        chart_type = self.chart_var.get() if not initial else "KD指標圖"
        time_option = self.time_var.get() if not initial else "1年"
        ticker = self.stock_dict.get(stock, None)
        if ticker:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.get_period(time_option))
            try:
                stock_data = yf.download(ticker, start=start_date, end=end_date)
                if stock_data.empty:
                    raise ValueError("Unable to fetch stock data")
                stock_data = stock_data[stock_data.index.dayofweek < 5]  # Only keep trading days
                if stock_data.empty:
                    raise ValueError("No data available for the given dates")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to fetch stock data: {e}")
                return
            
            chart_funcs = {
                "KD指標圖": plot_kd_chart,
                "均價指標圖": plot_ma_chart,
                "均量指標圖": plot_volume_chart,
                "RSI": plot_rsi,
                "常態分佈圖": plot_normal_distribution,
                "盒鬚圖": plot_boxplot,
                "熱力圖": plot_heatmap
            }

            plot_func = chart_funcs.get(chart_type, plot_kd_chart)
            plot_func(self, stock_data)

    def display_chart(self, fig):
        for widget in self.root.grid_slaves(row=0, column=2):
            widget.grid_forget()
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=6)

    def get_period(self, time_option):
        time_map = {"1月": 30, "3月": 90, "6月": 180, "1年": 365, "2年": 730}
        return time_map.get(time_option, 365)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()

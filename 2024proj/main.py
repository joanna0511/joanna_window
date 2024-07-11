import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt  # 導入 matplotlib 的 pyplot
from plot_methods import plot_kd_chart, plot_ma_chart
from plot_methods import plot_volume_chart, plot_normal_distribution 
  # 導入繪圖方法

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
        # 創建控件...
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
        # 繪圖邏輯...
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
            plot_kd_chart(self, stock_data)
        elif chart_type == "均價指標圖":
            plot_ma_chart(self, stock_data)
        # 其他繪圖調用類似...
        elif chart_type == "均量指標圖":
                self.plot_volume_chart(stock_data)
        elif chart_type == "常態分佈圖":
                self.plot_normal_distribution(stock_data)


    def display_chart(self, fig):
        # 顯示圖表...
        for widget in self.root.grid_slaves(row=0, column=2):
            widget.grid_forget()
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=6)


        

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()

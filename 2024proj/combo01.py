import tkinter as tk
from tkinter import ttk
import subprocess

# 創建主窗口
root = tk.Tk()
root.title("下拉選單示例")

# 標籤
label = ttk.Label(root, text="請選擇一個選項:")
label.pack(pady=10)

# 創建下拉選單
options = [1, 2, 3]
selected_option = tk.StringVar()

dropdown = ttk.Combobox(root, textvariable=selected_option, values=options)
dropdown.pack(pady=10)

# 初始選擇第一個選項
dropdown.current(0)

# 創建一個函數來處理按鈕點擊
def on_button_click():
    selected = selected_option.get()
    
    # 根據選擇執行不同的程式
    if selected == '1':
        subprocess.run(["python", "kd.py"])  # 執行 kd.py
    elif selected == '2':
        subprocess.run(["python", "priceMa.py"])  # 執行 priceMa.py
    elif selected == '3':
        subprocess.run(["python", "volumeMa.py"])  # 執行 volumeMa.py
    else:
        print(f'未知選項: {selected}')

# 創建按鈕
execute_button = ttk.Button(root, text="執行", command=on_button_click)
execute_button.pack(pady=10)

# 顯示結果的標籤
result_label = ttk.Label(root, text="")
result_label.pack(pady=10)

# 運行主循環
root.mainloop()

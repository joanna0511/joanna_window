import pandas as pd

# 讀取台積電的股價資料
file_path = './tsmcadr10y.csv'  # 替換為你的檔案路徑
tsmc_data = pd.read_csv(file_path)

# 去掉 '調整後收盤價 (Adj Close)' 欄位
tsmc_data_modified = tsmc_data.drop(columns=['Adj Close'])

# 另存成 tsmcadr10y-1.csv
new_file_path = './tsmcadr10y-1.csv'  # 替換為你要儲存檔案的路徑
tsmc_data_modified.to_csv(new_file_path, index=False)

print(f"已將修改後的資料儲存成 {new_file_path}")

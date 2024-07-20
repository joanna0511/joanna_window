import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# 讀取 NVIDIA 和 TSMC 的股價資料
nvidia_file_path = './nvidia10y.csv'  
tsmc_file_path = './tsmcadr10y.csv'   

nvidia_data = pd.read_csv(nvidia_file_path)
tsmc_data = pd.read_csv(tsmc_file_path)

# 確保日期欄位是日期類型，並設置為索引
nvidia_data['Date'] = pd.to_datetime(nvidia_data['Date'])
tsmc_data['Date'] = pd.to_datetime(tsmc_data['Date'])

nvidia_data.set_index('Date', inplace=True)
tsmc_data.set_index('Date', inplace=True)

# 合併兩個數據集，以日期為鍵
combined_data = pd.merge(nvidia_data['Close'], tsmc_data['Close'], left_index=True, right_index=True, suffixes=('_NVIDIA', '_TSMC'))

# 進行迴歸分析
X = combined_data['Close_NVIDIA']
y = combined_data['Close_TSMC']

X = sm.add_constant(X)  # 增加常數項
model = sm.OLS(y, X).fit()
predictions = model.predict(X)

# 繪製散點迴歸圖
plt.figure(figsize=(10, 6))
sns.regplot(x='Close_NVIDIA', y='Close_TSMC', data=combined_data)
plt.title('Regression Analysis: NVIDIA vs. TSMC ADR')
plt.xlabel('NVIDIA Closing Price')
plt.ylabel('TSMC ADR Closing Price')
plt.show()

# 列出分析結果相關參數
print(model.summary())

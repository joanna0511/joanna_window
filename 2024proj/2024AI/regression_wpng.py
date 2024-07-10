import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# 讀取CSV檔案
nvidia_data = pd.read_csv('NVIDIA_5years.csv')
tsmc_data = pd.read_csv('TSMC_5years.csv')

# 提取日期和收盤價
nvidia_data['Date'] = pd.to_datetime(nvidia_data['Date'])
tsmc_data['Date'] = pd.to_datetime(tsmc_data['Date'])

nvidia_close = nvidia_data[['Date', 'Close']]
tsmc_close = tsmc_data[['Date', 'Close']]

# 合併資料
merged_data = pd.merge(nvidia_close, tsmc_close, on='Date', suffixes=('_NVIDIA', '_TSMC')).dropna()

# 畫出散佈圖
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Close_NVIDIA', y='Close_TSMC', data=merged_data)
plt.title('NVIDIA vs TSMC Daily Closing Prices')
plt.xlabel('NVIDIA Closing Price')
plt.ylabel('TSMC Closing Price')
plt.grid(True)
plt.show()

# 回歸分析
X = merged_data['Close_NVIDIA'].values.reshape(-1, 1)
y = merged_data['Close_TSMC'].values

# 添加常數項以適應 statsmodels 的需求
X_sm = sm.add_constant(X)

# 建立 OLS 模型
model = sm.OLS(y, X_sm)
results = model.fit()

# 顯示回歸係數
print(f"回歸係數: {results.params[1]}")
print(f"截距: {results.params[0]}")

# 繪製回歸線
y_pred = results.predict(X_sm)

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Close_NVIDIA', y='Close_TSMC', data=merged_data)
plt.plot(merged_data['Close_NVIDIA'], y_pred, color='red', label='Regression Line')
plt.title('NVIDIA vs TSMC Daily Closing Prices with Regression Line')
plt.xlabel('NVIDIA Closing Price')
plt.ylabel('TSMC Closing Price')
plt.legend()
plt.grid(True)
plt.show()

# 顯示詳細的回歸分析結果
print(results.summary())

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
nvidia_df = pd.read_csv('nvidia10y-2_novolum_60ma.csv')
tsmc_df = pd.read_csv('tsmcard10y_2_novolumn_60ma.csv')

# 合并数据
merged_df = pd.merge(nvidia_df, tsmc_df, on='Date', suffixes=('_nvidia', '_tsmc'))

# 计算相关矩阵
correlation_matrix = merged_df.drop(columns=['Date']).corr()

# 绘制热力图
plt.figure(figsize=(12, 10))
plt.title('Heatmap of NVIDIA and TSMC Data')
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.show()

import pandas as pd
from sklearn.tree import DecisionTreeRegressor, plot_tree
import matplotlib.pyplot as plt

# 加載數據
nvidia_df = pd.read_csv('nvidia10y-2_novolum.csv')
tsmc_df = pd.read_csv('tsmcadr10y-2_novolum.csv')

# 合併數據
merged_df = pd.merge(nvidia_df, tsmc_df, on='Date', suffixes=('_nvidia', '_tsmc'))

# 準備數據
features = merged_df[['Open_nvidia', 'High_nvidia', 'Low_nvidia', 'Close_nvidia', '20MA_nvidia', '50MA_nvidia']].dropna()
labels = merged_df.loc[features.index, 'Close_tsmc']

# 訓練決策樹回歸模型
tree_model = DecisionTreeRegressor(max_depth=5)
tree_model.fit(features, labels)

# 繪製決策樹
plt.figure(figsize=(20, 10))
plot_tree(tree_model, feature_names=features.columns, filled=True, rounded=True, fontsize=10)
plt.title('Decision Tree for TSMC Closing Price Prediction based on NVIDIA Data')
plt.show()

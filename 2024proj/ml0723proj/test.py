import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# 加載數據
nvidia_df = pd.read_csv('nvidia10y-2_novolum_60ma.csv')
tsmc_df = pd.read_csv('tsmcard10y_2_novolumn_60ma.csv')

# 合併數據
merged_df = pd.merge(nvidia_df, tsmc_df, on='Date', suffixes=('_nvidia', '_tsmc'))

# 準備數據
features = merged_df[['Open_nvidia', 'High_nvidia', 'Low_nvidia', 'Close_nvidia', '20MA_nvidia', '60MA_nvidia']].dropna()
labels = merged_df.loc[features.index, 'Close_tsmc']

# 定義參數網格
param_grid = {
    'max_depth': [3, 5, 7, 10],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# 初始化決策樹回歸模型
tree_model = DecisionTreeRegressor()

# 使用 GridSearchCV 進行超參數調優
grid_search = GridSearchCV(estimator=tree_model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(features, labels)

# 獲取最佳模型
best_tree_model = grid_search.best_estimator_

# 繪製最佳決策樹
plt.figure(figsize=(20, 10))
plot_tree(best_tree_model, feature_names=features.columns, filled=True, rounded=True, fontsize=10)
plt.title('Optimized Decision Tree for TSMC Closing Price Prediction based on NVIDIA Data')
plt.show()

# 顯示最佳參數
print("Best parameters found: ", grid_search.best_params_)

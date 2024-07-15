import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree

def plot_price_chart(app, data_dict, tickers):
    fig, ax = plt.subplots(figsize=(8, 4))
    
    ticker = tickers if isinstance(tickers, str) else tickers[0]
    data = data_dict[ticker]['Close']
    data.plot(ax=ax, title=f'{ticker} 價格走勢圖')
    
    ax.set_xlabel('日期')
    ax.set_ylabel('價格')
    
    app.display_chart(fig)

def plot_scatter_chart(app, data_dict, tickers):
    fig, ax = plt.subplots(figsize=(8, 4))
    
    if len(tickers) == 2:
        data1 = data_dict[tickers[0]]['Close']
        data2 = data_dict[tickers[1]]['Close']
        merged_data = pd.DataFrame({tickers[0]: data1, tickers[1]: data2}).dropna()
        ax.scatter(merged_data[tickers[0]], merged_data[tickers[1]], label=f'{tickers[0]} vs {tickers[1]}')
    
        ax.set_xlabel(tickers[0])
        ax.set_ylabel(tickers[1])
    
    ax.set_title('散佈圖')
    if len(ax.get_legend_handles_labels()[1]) > 0:  # 檢查是否有圖例標籤
        ax.legend()
    app.display_chart(fig)

def plot_regression_chart(app, data_dict, tickers):
    fig, ax = plt.subplots(figsize=(8, 4))
    
    if len(tickers) == 2:
        data1 = data_dict[tickers[0]]['Close']
        data2 = data_dict[tickers[1]]['Close']
        merged_data = pd.DataFrame({tickers[0]: data1, tickers[1]: data2}).dropna()
        
        X = merged_data[tickers[0]].values.reshape(-1, 1)
        y = merged_data[tickers[1]].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        
        ax.scatter(merged_data[tickers[0]], merged_data[tickers[1]], label='Data points')
        ax.plot(merged_data[tickers[0]], y_pred, color='red', label='Regression line')
    
        ax.set_xlabel(tickers[0])
        ax.set_ylabel(tickers[1])
    
    ax.set_title('迴歸分析圖')
    if len(ax.get_legend_handles_labels()[1]) > 0:  # 檢查是否有圖例標籤
        ax.legend()
    app.display_chart(fig)

def plot_decision_tree(app, data_dict, tickers):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    if len(tickers) == 2:
        data1 = data_dict[tickers[0]]['Close']
        data2 = data_dict[tickers[1]]['Close']
        merged_data = pd.DataFrame({tickers[0]: data1, tickers[1]: data2}).dropna()
        
        X = merged_data[tickers[0]].values.reshape(-1, 1)
        y = (merged_data[tickers[1]].pct_change() > 0).astype(int)  # 生成漲跌標籤
        
        model = DecisionTreeClassifier(max_depth=3)
        model.fit(X, y)
        
        plot_tree(model, feature_names=[tickers[0]], class_names=['跌', '漲'], filled=True, ax=ax)
    
        ax.set_title('決策樹圖')
    
    app.display_chart(fig)

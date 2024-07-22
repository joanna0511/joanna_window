import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Load TSMC's (2330.TW) stock data
file_path = '/mnt/data/ts2330_5y.csv'
data = pd.read_csv(file_path)

# Calculate Z-scores
data['Z-score'] = (data['Close'] - data['Close'].mean()) / data['Close'].std()

# Plot the probability density function of Z-scores
plt.figure(figsize=(10, 6))
sns.histplot(data['Z-score'], kde=True, stat="density", linewidth=0)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, 0, 1)
plt.plot(x, p, 'k', linewidth=2)
title = "Probability Density Function of TSMC (2330.TW) Z-scores (5 years)"
plt.title(title)
plt.xlabel('Z-score')
plt.ylabel('Density')
plt.grid(True)
plt.show()

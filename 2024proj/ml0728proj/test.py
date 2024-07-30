# Importing required library for Z-score calculation
from scipy import stats

# Calculate the Z-scores for the 'Close' prices and 'Volume'
nvidia_df['Close_zscore'] = stats.zscore(nvidia_df['Close'])
nvidia_df['Volume_zscore'] = stats.zscore(nvidia_df['Volume'])

tsmc_df['Close_zscore'] = stats.zscore(tsmc_df['Close'])
tsmc_df['Volume_zscore'] = stats.zscore(tsmc_df['Volume'])

# Identify rows with Z-scores higher than 3 or lower than -3 (considered as potential outliers)
nvidia_outliers = nvidia_df[(nvidia_df['Close_zscore'].abs() > 3) | (nvidia_df['Volume_zscore'].abs() > 3)]
tsmc_outliers = tsmc_df[(tsmc_df['Close_zscore'].abs() > 3) | (tsmc_df['Volume_zscore'].abs() > 3)]

# Display the identified outliers
nvidia_outliers, tsmc_outliers

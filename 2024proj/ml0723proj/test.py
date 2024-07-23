import pandas as pd

# Load the provided CSV file
tsmc_df = pd.read_csv('tsmcadr10y.csv')

# Remove 'Adj Close' and 'Volume' columns
tsmc_df = tsmc_df.drop(columns=['Adj Close', 'Volume'])

# Calculate the 20-day and 60-day moving averages for TSMC dataframe
tsmc_df['20MA'] = tsmc_df['Close'].rolling(window=20).mean()
tsmc_df['60MA'] = tsmc_df['Close'].rolling(window=60).mean()

# Save the modified TSMC dataframe to a new CSV file
tsmc_df.to_csv('tsmcard10y_2_novolumn_60ma.csv', index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Modified TSMC ADR Data with 20MA and 60MA", dataframe=tsmc_df)

tsmc_df.head(25)

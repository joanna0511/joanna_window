# Remove the Volume column from TSMC dataframe
tsmc_df = tsmc_df.drop(columns=['Volume'])

# Calculate the 20-day and 50-day moving averages for TSMC dataframe
tsmc_df['20MA'] = tsmc_df['Close'].rolling(window=20).mean()
tsmc_df['50MA'] = tsmc_df['Close'].rolling(window=60).mean()

# Save the modified TSMC dataframe to a new CSV file
tsmc_df.to_csv('/mnt/data/tsmcadr10y-2.csv', index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Modified TSMC ADR Data", dataframe=tsmc_df)

tsmc_df.head(25)

# Purpose: Filter, aggregate, and summarise high-value orders by country.
# Inputs: data/orders.csv
# Outputs: country-level total_value summary (filtered > 100), saved to CSV + row count printed

import pandas as pd
from pathlib import Path


script_dir = Path(__file__).resolve().parent
data_dir = script_dir / "data"

df = pd.read_csv(data_dir/'orders.csv')

# Adds total_value (quantity × unit_price)
df['total_value'] = round(df['quantity'] * df['unit_price'],2 )
# Filters to orders where total_value is greater than 100
df_filtered = df[df['total_value'] > 100]
# Groups by country and sums the total_value per country
df_filtered.groupby('country')['total_value'].sum()
# Sorts from highest to lowest
df_filtered.sort_values('total_value', ascending=False)  
# Writes the result to data/country_summary.csv
df_filtered.to_csv(data_dir/'country_summary.csv', index=False)
# Prints how many rows made it through the filter
print("The number of rows made it through the filter = ", df_filtered.shape[0])
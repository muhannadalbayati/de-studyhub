# Purpose: Summarise order data using group-based aggregations.
# Inputs: data/orders.csv
# Outputs: Quantity by country, average price by category, order count by country

import pandas as pd
from pathlib import Path


script_dir = Path(__file__).resolve().parent
data_dir = script_dir / "data"

df = pd.read_csv(data_dir/'orders.csv')

# Total quantity sold per country
print("Total quantity sold per country")
print(df.groupby('country')['quantity'].sum())
print("----------------------------------------------------")
# Average unit price per product category
print("Average unit price per product category")
print(round(df.groupby('product_category')['unit_price'].mean(),2))
print("----------------------------------------------------")
# Number of orders per country
print("Number of orders per country")
print(df.groupby('country')['order_id'].sum())
print("----------------------------------------------------")


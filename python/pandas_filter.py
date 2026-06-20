# Purpose: Load and filter order data from a CSV file.
# Inputs: data/orders.csv
# Outputs: UK orders, quantity > 5 orders, UK orders with quantity > 5

import pandas as pd
from pathlib import Path


script_dir = Path(__file__).resolve().parent
data_dir = script_dir / "data"

df = pd.read_csv(data_dir/'orders.csv')

# All orders from the UK
print("All orders from the UK")
print(df[df['country'] == 'UK'])
print("--------------------------------------------------------------")
# All orders where quantity is greater than 5
print("All orders where quantity is greater than 5")
print(df[df['quantity'] > 5])
print("--------------------------------------------------------------")
# All orders from the UK where quantity is greater than 5
print("All orders from the UK where quantity is greater than 5")
print(df[(df['country'] == 'UK') & (df['quantity'] > 5)])
print("--------------------------------------------------------------")
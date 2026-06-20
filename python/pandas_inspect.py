# Purpose: Load and explore the orders dataset to understand its structure, contents, and basic distribution of data.
# Inputs: pandas library and the data/orders.csv file.
# Outputs: First 5 rows of data, dataset shape (rows and columns), column names with data types, and the count of orders from each country.

import pandas as pd
from pathlib import Path


script_dir = Path(__file__).resolve().parent
data_dir = script_dir / "data"

df = pd.read_csv(data_dir/'orders.csv')

# Prints the first 5 rows
print("The first 5 rows on the dataset are:")
print(df.head())
print("--------------------------------------------------------------")
# Prints the shape (rows, columns)
print("The number of rows and columns in the data set are: ", df.shape)
# Prints the column names and their data types
print("Here is the data types of each column in the DataFrame")
print(df.dtypes)
print("--------------------------------------------------------------")
# Prints a count of how many orders came from each country 
print("Number of orders per country")
print(df.groupby('country')['order_id'].count())

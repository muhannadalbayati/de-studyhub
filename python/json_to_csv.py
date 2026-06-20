# Purpose:  Read from JSON, process data by filtering and performing some calculations, 
#           Save the resulted data to a CSV file.
# Methods:  Using Python Dictoinary to manipulate data. Read from JSON and write on CSV 
# Concepts: Iteraition, Dictonary, Import libraries, handling data files, 
#           Pathlib module, JSON library, CSV library, subroutine (functions)
# Input:    data/products.json
# Output:   data/instock_summary.csv

# Importing the reuired libraries
from pathlib import Path
import json
import csv

# Declaring, initialisng and setting global variables and constants
script_dir = Path(__file__).resolve().parent
data_dir = script_dir.parent / "data"

def readJSON(data_file):
    """
        reading data from JSON file, save it to a dictionary, pass it back to the main
    """
    with open(data_dir / data_file, "r") as f:
        products = json.load(f)
    return(products)

def writeCSV(para_filtered_products): 
    """ 
        receive the data from the main, calculate the total stock value, save the data on a new CSV file
    """  
    headers = ['product', 'category', 'price', 'quantity', 'total_stock_value']
    
    with open(data_dir /"instock_summary.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for product in para_filtered_products:       
            writer.writerow({
                'product': product['product'],
                'category': product['category'],
                'price': product['price'],
                'quantity': product['quantity'],
                'total_stock_value': str(round(product['price'] * product['quantity'],2))
            })          
    return(True)

def readCSV(data_file):
    """ 
        Read from CSV file, save in a dictionary variable (row), 
        pass the variable back to the main
    """
    with open(data_dir / data_file , newline='') as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)    
    return (rows)


# Read the products and filter the in stock products
filtered_products = []
products = readJSON('products.json')
for product in products:
    if product['in_stock'] == True:
        filtered_products.append(product)

# Write the filtered data into a CSV file
writeCSV(filtered_products)

rows = readCSV("instock_summary.csv")
for row in rows:
    print(row)




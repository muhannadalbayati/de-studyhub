# Purpose:  Read/ write products data from/to json file.
# Methods:  Using Python Dictoinary to manpulate data from/to the json file
# Concepts: Iteraition, Dictonary, Import libraries, handling data files, 
#           Pathlib module, JSON library, subroutine (functions)
# Input:    data/products.json
# Output:   data/products_instock.json

# Importing the reuired libraries
from pathlib import Path
import json

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

def writeJSON(para_filtered_products):
    """
        Receive data from the main program in a form of a list. Save the data to a JSON file
    """
    with open(data_dir / 'products_instock.json', "w") as f:
        json.dump(para_filtered_products, f, indent=4)  
    return(True)

filtered_products = []
products = readJSON('products.json')
print("All products:")
for product in products:
    print(product)
print("=============================================")
print("Products in stock:")
for product in products:
    if product['in_stock'] == True:
        filtered_products.append(product)
        print(product)

writeJSON(filtered_products)




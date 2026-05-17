# Purpose:  Read sales data from CSV, calculate total value per product,
#           and write a summary CSV to the data folder.
# Methods:  Using Python Dictoinary to manpulate data from/to CSV file
# Concepts: Iteraition, Dictonary, Import libraries, handling data files, 
#           Pathlib module, CSV Module, subroutine (functions)
# Input:    data/sales.csv
# Output:   data/sales_summary.csv

# Importing the reuired libraries
from pathlib import Path
import csv

# Declaring, initialisng and setting global variables and constants
script_dir = Path(__file__).resolve().parent
data_dir = script_dir.parent / "data"

def readCSV(dataFile):
    """ 
        Read from CSV file, save in a dictionary variable (row), 
        pass the variable back to the main
    """
    with open(data_dir / dataFile , newline='') as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)    
    return (rows)
# ==========================================================

# Creating a dictionalry and saving the content into a CSV file
def writeCSV(rows): 
    """ 
        receive the data from the main, calculate the total price, the data on a new CSV file
    """  
    headers = ['product', 'quantity', 'price', 'total_value']
    
    with open(data_dir /"sales_summary.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:       
            writer.writerow({
                'product': row['product'],
                'quantity': row['quantity'],
                'price': row['price'],
                'total_value': str(round(float(row['price']) * int(row['quantity']),2))
            })          
    return(True)


# Main Program
dataFile = "sales.csv"
rows = readCSV(dataFile)
for row in rows:
    print(row)
    
writeCSV(rows)

dataFile = "sales_summary.csv"
rows = readCSV(dataFile)
for row in rows:
    print(row)


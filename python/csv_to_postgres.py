# Purpose: Reads sales.csv and loads each row into the sales table in de_practice PostgreSQL database.
# Input:   data/sales.csv — columns: product, quantity, price
# Output:  sales table populated in de_practice, row count printed to console

import csv
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

script_dir = Path(__file__).resolve().parent
data_file = script_dir / "data" / "sales.csv"


def get_connection():
    """Creates and returns a connection to the de_practice database.
    Credentials loaded from .env — never hardcoded.
    Returns: psycopg2 connection object"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def create_table(cursor):
    """Creates the sales table if it does not already exist.
    Args: cursor — active psycopg2 cursor
    Returns: None"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id       SERIAL PRIMARY KEY,
            product  VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL,
            price    NUMERIC(10,2) NOT NULL
        );
    """)


def load_csv(cursor):
    """Reads sales.csv and inserts each row into the sales table.
    Uses parameterised INSERT — values are never concatenated into the SQL string.
    Args: cursor — active psycopg2 cursor
    Returns: int — number of rows inserted"""
    count = 0
    with open(data_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                "INSERT INTO sales (product, quantity, price) VALUES (%s, %s, %s);",
                (row['product'], int(row['quantity']), float(row['price']))
            )
            count += 1
    return count


conn = get_connection()
cursor = conn.cursor()

create_table(cursor)
rows_inserted = load_csv(cursor)

conn.commit()
cursor.close()
conn.close()

print(f"{rows_inserted} rows inserted into sales table.")

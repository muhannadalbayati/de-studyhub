# Purpose: Connects to the de_practice PostgreSQL database and runs a test query.
# Input:   .env file with database credentials
# Output:  Prints all customers and their countries to the console

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    """Creates and returns a connection to the de_practice database.
    Credentials are loaded from .env — never hardcoded.
    Returns: psycopg2 connection object"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def fetch_customers():
    """Fetches all customers from the customers table.
    Returns: list of tuples (customer_id, name, country)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, name, country FROM customers ORDER BY customer_id;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

customers = fetch_customers()
for row in customers:
    print(f"ID: {row[0]} | Name: {row[1]} | Country: {row[2]}")

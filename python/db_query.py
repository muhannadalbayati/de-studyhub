# Purpose: Demonstrates parameterised queries against the de_practice PostgreSQL database.
# Input:   .env file with database credentials, country filter passed as parameter
# Output:  Prints customers from a given country and their total spend

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

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

def fetch_customers_by_country(country):
    """Fetches all customers from a given country using a parameterised query.
    The %s placeholder is filled safely by psycopg2 — never by string formatting.
    Args:    country (str) — the country to filter by
    Returns: list of tuples (name, country)"""
    conn = get_connection()
    cursor = conn.cursor()

    # CORRECT — parameterised query. psycopg2 handles escaping safely.
    cursor.execute(
        "SELECT name, country FROM customers WHERE country = %s ORDER BY name;",
        (country,)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_spend_by_country(country):
    """Fetches total spend per customer for a given country.
    Args:    country (str) — the country to filter by
    Returns: list of tuples (name, total_spent)"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT customers.name, SUM(orders.amount) AS total_spent
        FROM customers
        JOIN orders ON customers.customer_id = orders.customer_id
        WHERE customers.country = %s
        GROUP BY customers.name
        ORDER BY total_spent DESC;
        """,
        (country,)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# --- Run both queries ---

country_filter = "UK"

print(f"Customers in {country_filter}:")
for row in fetch_customers_by_country(country_filter):
    print(f"  {row[0]} — {row[1]}")

print(f"\nTotal spend by {country_filter} customers:")
for row in fetch_spend_by_country(country_filter):
    print(f"  {row[0]}: £{row[1]}")

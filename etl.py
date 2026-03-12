import sqlite3
import csv
from pathlib import Path

"""
    TODO:
        - look into using csv for writing to a csv file, its not necessary but would like to have it sorted
"""

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # taking the place of user_config_path for a generalised output path, I have it outputting
# to the cloned repo as I don't want to clog your documents folder (or similar) or if the uni perms will allow/disallow certain output
# locations
CSV_FILE = OUTPUT_DIR / Path("output.csv")

def fetch() -> list[dict]:

    conn = sqlite3.connect("customers.db")
    c = conn.cursor()

    c.execute("SELECT customers.customer_id, customers.first_name, customers.family_name, orders.quantity, orders.unit_price FROM customers LEFT JOIN orders ON customers.customer_id = orders.customer_id WHERE customers.status = 'active'")
    rows = c.fetchall()
    conn.close()

    customers = {}

    # this, not to toot my own horn, is a little genuis. I got stuck on how to do this cleanly for a while, as sqlite just returns a list of
    # tuples irrespective of whether there's repeats, so I use the customer_id itself as the key and set the rest of the data as the value
    # mixed in with a little tuple unpacking (this feels like when I learnt list comprehension and generator expressions, it's crazy) though
    # i fear this is probably just common knowledge
    for row in rows: 
        customer_id, first_name, family_name, quantity, unit_price = row

        if customer_id not in customers:
            customers[customer_id] = {"customer_id": customer_id, "first_name": first_name, "family_name": family_name, "orders": []}

        if quantity is not None:
            customers[customer_id]["orders"].append({"quantity": quantity, "unit_price": unit_price})

    return list(customers.values())

active_customers = fetch()

customers = {}

with open(CSV_FILE, "w+", newline="") as csv_file:
    fieldnames = "name,total order value"
    csv_file.write(f"{fieldnames}\n")
    #writer = csv.writer(csv_file)
    for active_customer in active_customers:
        order_total = 0
        customer = f"{active_customer['first_name']} {active_customer['family_name']}"
        for order in active_customer["orders"]:
            order_total = order_total + order["quantity"] * order["unit_price"]

        csv_file.write(f"{customer},{order_total}\n")


"""
tuple unpacking... why have I never seen this before https://www.w3schools.com/python/python_tuples_unpack.asp

initially was going to the use the csv module as it's what I used before but it would write the data as "a,l,i,c,e ..." I'm not entirely
sure why but this is the exact result I would want anyway
"""
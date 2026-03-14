import sqlite3
import csv
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_FILE = OUTPUT_DIR / Path("output.csv")

def fetch() -> list[dict]:
    """ fetches customers with 'active' statuses """

    conn = sqlite3.connect("customers.db")
    c = conn.cursor()

    c.execute("""SELECT customers.customer_id, 
              customers.first_name, 
              customers.family_name, 
              orders.quantity, 
              orders.unit_price 
              FROM customers 
              LEFT JOIN orders 
              ON customers.customer_id = orders.customer_id 
              WHERE customers.status = 'active'
              """)
    
    rows = c.fetchall()
    conn.close()

    customers = {}

    for row in rows: 
        customer_id, first_name, family_name, quantity, unit_price = row # tuple unpack 

        if customer_id not in customers: # uses the customer_id as an index then if it's not included in the dictionary, set the entireity as a value
            customers[customer_id] = {"customer_id": customer_id, "first_name": first_name, "family_name": family_name, "orders": []}

        if quantity is not None: # if quantity when unpacked isn't empty, assign the current customer
            customers[customer_id]["orders"].append({"quantity": quantity, "unit_price": unit_price})

    return list(customers.values()) # removes the customer_id keys and sends back a list of dictionaries

def transform_and_load():
    """ transforms customer data and loads into a csv file """

    customers = fetch()

    with open(CSV_FILE, "w+", newline="") as csv_file:
        fieldnames = "name,total order value" # column headers for csv
        csv_file.write(f"{fieldnames}\n")

        for customer in customers:
            order_total = 0
            c_name = f"{customer['first_name']} {customer['family_name']}"
            for order in customer["orders"]:
                order_total = order_total + order["quantity"] * order["unit_price"]
                csv_file.write(f"{c_name},{order_total}\n") 
                # looking back at the task, I think I misunderstood, you want each customer's induvidual orders as a sum and row as apposed to the
                # entire value of ALL of a customer's orders (I did think that was a little weird)

            #csv_file.write(f"{customer},{order_total}\n")

if __name__ == "__main__":
    transform_and_load()

"""
tuple unpacking... why have I never seen this before https://www.w3schools.com/python/python_tuples_unpack.asp

initially was going to the use the csv module as it's what I used before but it would write the data as "a,l,i,c,e ..." I'm not entirely
sure why but this is the exact result I would want anyway
"""
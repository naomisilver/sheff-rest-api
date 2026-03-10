import sqlite3
import os
import json
from pathlib import Path

DB_PATH = "customers.db"
CUSTOMERS_DATA = Path("data") / "customers.json"
ORDERS_DATA = Path("data") / "orders.json"

"""
    TODO:
        - move db intialisation from __init__ only and have an explicit call to create_db, if api.py is called before db.py a malformed customers.db is created 
          (I could have api.py create a db object meaning it would be created before flask runs but the requirements were to make "a script" which i interpret 
          as single run)
"""

class Database:
    def __init__(self):

        if not os.path.exists(DB_PATH):
            self.create_db()

    def create_db(self):

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""CREATE TABLE customers (
                          customer_id integer PRIMARY KEY,
                          first_name text NOT NULL,
                          family_name text,
                          email text NOT NULL UNIQUE,
                          status text NOT NULL CHECK(status = "archived" OR status = "active" OR status = "suspended")
                          )
                        """)
        
        c.execute("""CREATE TABLE orders (
                          order_id integer PRIMARY KEY,
                          customer_id integer NOT NULL,
                          product_name text NOT NULL,
                          product_barcode integer NOT NULL UNIQUE,
                          quantity integer NOT NULL,
                          unit_price numeric NOT NULL,
                          FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
                          )
                        """)
        
        conn.commit()
        conn.close()

    def populate_customers(self, customers: list[dict]):
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.executemany("""INSERT OR IGNORE INTO customers (
                  first_name,
                  family_name,
                  email,
                  status
                  )
                  VALUES (:first_name, :family_name, :email, :status)
                """,
                    customers
                )
        
        conn.commit()
        conn.close()

    def populate_orders(self, orders: list[dict]):

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.executemany("""INSERT OR IGNORE INTO orders (
                      customer_id,
                      product_name,
                      product_barcode,
                      quantity,
                      unit_price
                      )
                      VALUES (:customer_id, :product_name, :product_barcode, :quantity, :unit_price)
                """,
                    orders
                )
        
        conn.commit()
        conn.close()


db = Database()

with open(CUSTOMERS_DATA, "r") as f:
    customers = json.load(f)

with open(ORDERS_DATA, "r") as f:
    orders = json.load(f)

db.populate_customers(customers)
db.populate_orders(orders)

        
"""
CHECK constraint: https://stackoverflow.com/questions/23920332/how-can-i-write-a-check-constraint-in-sql-that-allows-a-series-of-strings-or-a-b
https://www.tutorialspoint.com/sqlite/sqlite_constraints.htm#:~:text=Constraints%20are%20the%20rules%20enforced,the%20data%20in%20the%20database.

list of dictionary inserts: https://stackoverflow.com/questions/70548095/when-trying-to-convert-a-list-of-python-dictionaries-into-a-sqlite-table-i-keep
    - I tried: https://stackoverflow.com/questions/33636191/insert-a-list-of-dictionaries-into-an-sql-table-using-python
      but sqlite3's implementation is different and doesn't use the %s formatting for dict items

added barcode column so I have something to conflict on, I *could've* used the product name as the unique and it would've been fine on this small of a scale
but plan for the future and all that
"""
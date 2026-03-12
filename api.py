import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

"""
    TODO:
        - add error handling for 404 and 400 

        - mirror the tuple unpacking I did in etl.py
            - unsure if I can/can't do tuple unpacking as I'm addressing specific
"""

@app.route("/orders", methods=['GET'])
def get_items():

    customer_id = request.args.get("customer_id")

    conn = sqlite3.connect("customers.db")
    c = conn.cursor()
    c.execute("SELECT * FROM customers LEFT JOIN orders ON customers.customer_id = orders.customer_id WHERE customers.customer_id = ?", (customer_id,))
    rows = c.fetchall()
    conn.close()

    customer = {"customer_id": rows[0][0], "first_name": rows[0][1], "family_name": rows[0][2], "email": rows[0][3], "status": rows[0][4], "orders": []}

    for row in rows:
        if row[5]: # doesn't attempt to assign orders if none exist
            customer["orders"].append({"order_id": row[5], "customer_id": row[6], "product_name": row[7], "product_barcode": row[8], "quantity": row[9], "unit_price": row[10]})

    return customer

# copied but adapted from etl.py to serve etl-alt.py so instead of querying just for the necessary information in SQL, I query it all but structure it much the
# same but to serve an API endpoint. Though, serving the same information as the /items endpoint, and creating an entire endpoint for it seems wasteful, this
# be better done through checking what search param is given so instead of "orders?customer_id=1" you would do "orders?status=active" to invoke, will look into
# this :D
@app.route("/status", methods=['GET'])
def get_status():

    status = request.args.get("status")

    conn = sqlite3.connect("customers.db")
    c = conn.cursor()
    c.execute("SELECT * FROM customers LEFT JOIN orders ON customers.customer_id = orders.customer_id WHERE customers.status=?", (status,))
    rows = c.fetchall()
    conn.close()

    customers = {}

    for row in rows: 
        customer_id, first_name, family_name, email, status, order_id, order_customer_id, product_name, product_barcode, quantity, unit_price = row

        if customer_id not in customers:
            customers[customer_id] = {"customer_id": customer_id, "first_name": first_name, "family_name": family_name, "email": email, "orders": [], "status": status}

        if quantity is not None:
            customers[customer_id]["orders"].append({"order_id": order_id, "customer_id": order_customer_id, "product_name": product_name, "product_barcode": product_barcode, "quantity": quantity, "unit_price": unit_price})

    return list(customers.values())

if __name__ == '__main__':
    app.run(debug=True)

"""
flask intro https://dzone.com/articles/build-simple-api-with-python-flask-and-sql
flask get params https://www.browserstack.com/guide/flask-get-query-parameters

refresher on join types in sql (mostly sqlite as sqlite only supports some of SQLs joins) led me to inner vs left join and an explanation far better than that I got
at universit, inner join pulls information only when data matches in both tables, like the centre of a venn diagram, left pulls information if it matches in the
left table, then from the other table if there is any

"""
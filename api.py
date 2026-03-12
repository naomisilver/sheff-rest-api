import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

"""
    TODO:
        - add a add error handling for 404 and 400 

        - mirror the tuple unpacking I did in etl.py
"""

@app.route("/orders", methods=['GET'])
def get_items():

    customer_id = request.args.get("customer_id")

    conn = sqlite3.connect("customers.db")
    c = conn.cursor()
    #c.execute("SELECT * FROM customers WHERE customer_id=?", (customer_id,))
    c.execute("SELECT * FROM customers LEFT JOIN orders ON customers.customer_id = orders.customer_id WHERE customers.customer_id = ?", (customer_id,))
    rows = c.fetchall()
    conn.close()

    customer = {"customer_id": rows[0][0], "first_name": rows[0][1], "family_name": rows[0][2], "email": rows[0][3], "status": rows[0][4], "orders": []}

    for row in rows:
        if row[5]: # doesn't attempt to assign orders if none exist
            customer["orders"].append({"order_id": row[5], "customer_id": row[6], "product_name": row[7], "product_barcode": row[8], "quantity": row[9], "unit_price": row[10]})

    return customer

if __name__ == '__main__':
    app.run(debug=True)

"""
flask intro https://dzone.com/articles/build-simple-api-with-python-flask-and-sql
flask get params https://www.browserstack.com/guide/flask-get-query-parameters

refresher on join types in sql (mostly sqlite as sqlite only supports some of SQLs joins) led me to inner vs left join and an explanation far better than that I got
at universit, inner join pulls information only when data matches in both tables, like the centre of a venn diagram, left pulls information if it matches in the
left table, then from the other table if there is any

"""
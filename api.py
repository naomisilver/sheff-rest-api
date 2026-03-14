import sqlite3
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.route("/customers", methods=['GET'])
def get_customers():
    """ starts the API """

    customer_id = request.args.get("customer_id")
    status = request.args.get("status")

    conn = sqlite3.connect("customers.db")
    c = conn.cursor()

    if customer_id: # if customer_id is given as an argument
        c.execute("""SELECT * FROM customers 
                  LEFT JOIN orders 
                  ON customers.customer_id = orders.customer_id 
                  WHERE customers.customer_id = ?""", 
                  (customer_id,)
                  )
    
    elif status: # if status is given as an argument
        c.execute("""SELECT * FROM customers 
                  LEFT JOIN orders 
                  ON customers.customer_id = orders.customer_id 
                  WHERE customers.status=?""", 
                  (status,)
                  )

    else: # if no args are given
        abort(400, "No search method provided")

    rows = c.fetchall()
    conn.close()

    customers = {}

    # the same data formatting used in etl.py 
    for row in rows: 
        customer_id, first_name, family_name, email, status, order_id, order_customer_id, product_name, product_barcode, quantity, unit_price = row

        if customer_id not in customers:
            customers[customer_id] = {"customer_id": customer_id, "first_name": first_name, "family_name": family_name, "email": email, "orders": [], "status": status}

        if quantity is not None:
            customers[customer_id]["orders"].append({"order_id": order_id, "customer_id": order_customer_id, "product_name": product_name, "product_barcode": product_barcode, "quantity": quantity, "unit_price": unit_price})

    return jsonify(list(customers.values()))

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=5000, debug=True) network test for fun
    #app.run(debug=True)
    app.run()

"""
flask intro:                        https://dzone.com/articles/build-simple-api-with-python-flask-and-sql
flask get params:                   https://www.browserstack.com/guide/flask-get-query-parameters

refresher on join types in sql (mostly sqlite as sqlite only supports some of SQLs joins) led me to inner vs left join and an explanation far better than that I got
at universit, inner join pulls information only when data matches in both tables, like the centre of a venn diagram, left pulls information if it matches in the
left table, then from the other table if there is any

multi params per singular endpoint: https://www.geeksforgeeks.org/python/using-request-args-for-a-variable-url-in-flask/
"""
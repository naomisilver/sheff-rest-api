import requests
import json
import sys
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_FILE = OUTPUT_DIR / Path("output-alt.csv")

API_ROOT = "http://127.0.0.1:5000/"

headers = {
        'user-agent': "sheffield-rest-api" # I'm not checking this in flask but good practice
    }

session = requests.Session() # not necessarily needed as I'm making a single call, and so maintaining the same session across invocations has little benefit

def get_status(status: str):
    
    payload = {
        "status": status
    }

    r = session.get(f"{API_ROOT}customers", headers=headers, params=payload)
    #print(r.status_code)

    data = r.json()

    return data

def transform():
    try:
        status = sys.argv[1]
    except IndexError:
        print("provide a status type: 'active', 'suspended' or 'archived'")
        raise SystemExit

    customers = get_status(status)

    with open(CSV_FILE, "w+", newline='') as csv_file:
        fieldnames = "name,total order value"
        csv_file.write(f"{fieldnames}\n")

        for customer in customers:
            order_total = 0

            c_name = f"{customer['first_name']} {customer['family_name']}"
            for order in customer["orders"]:
                order_total = order_total + order["quantity"] * order["unit_price"]

            csv_file.write(f"{c_name},{order_total}\n")

if __name__ == "__main__":
    transform()

"""
I thought this would be nice: https://www.tutorialspoint.com/python/python_command_line_arguments.htm#:~:text=You%20can%20pass%20values%20to,argv%20variable.
"""
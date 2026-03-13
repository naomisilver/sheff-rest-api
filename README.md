# sheff-rest-api

my take on the first stage task, while not part of the task, I did have a little fun with it and create a `etl-alt` script which performs the same steps as `etl.py`. But instead of accessing the database directly, it invokes the API. This wasn't a requirement but this task is very well alligned with a project I'm currently working on [here](https://github.com/naomisilver/mediamultitool).


## Package dependencies
- ***Flask***
- ***Requests*** (only required for `etl-alt.py`)

#### Dependency Installation:

- Linux:
    - You'll need to use venv with `python3 -m venv /path/to/virtual/enviroment`, then cd to the cloned repo and run: `source [venv root dir]/bin/activate`
    - `pip install flask requests`

*Example*:

```bash
cd Downloads
git clone https://github.com/naomisilver/sheff-rest-api.git
cd sheff-rest-api
python3 -m venv .venv/
source .venv/bin/activate
pip install flask requests
```

> This will create a virtual enviroment in my repo, if you have one already setup elsewhere that works too :), just adapt the paths in later commands.

- Windows:
    - In powershell/cmd, `pip install flask requests`

- MacOS:
    - *I don't have a way to verify installation/usage instructions on MacOS though they should follow closely to the Linux instructions*
---

## Usage Instructions

> Instructions are applicable to both Linux and Windows where a venv instance is required in Linux and optional in Windows

### `db.py`:

Run the following in powershell. This creates the database and populates the database from the datasets: `data/customers.json` and `data/orders.json`.

- ```bash
  python db.py
  ```

### `api.py`: 

Run the following command. This starts the API with the endpoint `/customers`. This will script will need to be active while invoking the API and if you run `etl-alt.py`

- ```bash 
  python api.py
  ```

To invoke the API you can either enter the following into a browser, `127.0.0.1:5000/customers?customer_id=?` where `?` is replaced with a `customer_id` to search for. Or within your terminal/powershell, use:

- ```bash
  Powershell/cmd:
  curl.exe htpp://127.0.0.1:5000/customers?customer_id=1
  ```

- ```bash
  Linux terminal:
  curl http://127.0.0.1:5000/customers?customer_id=1
  ```

> There is also the ability to pass the argument `...?status=active` to this endpoint to instead return all customers with the matching status, the possible options are "active", "suspended" and "archived"

### `etl.py`:

To run the etl script run the following command:

- ```bash
  python etl.py
  ```

This will create an output directory in this cloned repository and an `output.csv` file with a customer's full name and their total order value.

> I could've used a package like `platformdirs` to get a platform agnostic Documents path or similar but with this likely being reveiwed on the universities network, I can't account for permissions, thus using the cloned repo as the output path is the safest options.

### `etl-alt.py`

> this was me having a bit of fun, incorporating my knowledge learnt in my project `mediamultitool` and using the `requests` package to invoke the API for the data requested in 'Task 3'.

To run the alternative etl script, run:

- ```
  python etl-alt.py [status type]
  ```

Where `[status type]` can either be `active`, `suspended` or `archived` and it will create an `output-alt.csv` file with each customers full name and order total with the matching status.

---

## My choices and reasoning:

### Package choice:
- With the task requiring data on customers AND their orders, a relational database was the obvious choice and as I have experience using `Sqlite3` I had opted for that. 
    - Further to this point, as a customer can have more than one order, a many-to-one relationship to an orders table, using the primary key `customer_id` as a foreign key to the orders table means I retain data integrity with no repeats.
    - Sqlite3 itself was chosen as it supports all of the SQL features necessary for this project and again, I have some experience using it.
    - Why no NoSQL? The schema necessary to fulfill the requirements is highly relational, structured and moderately small.

- As for the RESTful package options, about the only package I could find, was `Flask`. Reddit threads and StackOverflow posts were filled with recommendations and documentation and I'm not one to look a gift horse in the mouth when it comes to great options.

- `Requests`, this is only used in `etl-alt.py` but is similar to `flask` in it's supposed fame. When I first started using APIs in my `mediamultitool` project, I was looking into the ways to evoke them and frameworks built around `Requests` or `httpx` like [pylast](https://github.com/pylast/pylast). And quickly got bottlenecked by their limited capability like (the lack of) session pooling, finer control over the payload and parallelisation, and looked at `Requests` and it is easy to use and incredibly feature rich.

### Code/data specific reasoning:

- In the dataset, I opted not to include the `customer_id` and `order_id` primary keys and rely on the auto incrementing key when inserting into the database. Because in this situation, I feel the `customer_id` value itself is not important and is used as a conflict along with `email`. However, in a database of students with a `student_id`, the ID would be used to address them in many different enviroments is more known to the student, whereas a customer wouldn't really know their ID in the database. (at least this was my experience at univerisity where my email was just my student ID)

- I added a `product_barcode` column to use as the unique order identifier initially as I misread the guidelines in the database setup task and just opted to keep it, looking back, if I used it as a conflict point it would not have allowed multiple orders of the same product. 

- I made a database class because I did want to make a more cohesive package on a different branch and I may still, and I did also approach this problem with the intention to create a `db` object in each `api.py` and `etl.py` to ensure the database was always correctly created and populated before attempting access but when looking further to *Task 3* where it says *"...a standalone script..."* I assumed this was the intention for all python scripts.

## Application flow:

### Schema:

![Database schema](/images/schema.png)

The application begins with creating the database and required tables for `Customers` and `Orders` using SQLite. Within the same script, sample data is then loaded in from `data/customers.json` and `data/orders.json`. And to meet the constraints, is designed to be recreated and repopulated on every execution. 

Once the database has been created and populated, the REST API provides access to the stored data. When the endpoint `/customers` is invoked, it runs a query to pull data matching the query from both the customers table and orders table matching either to a `customer_id` or customer's `status` based on the arguments passed in the payload.

The `etl.py` script directly queries the database which extracts customer and order data, transforms it by combining a customer's first and family name into a single customer name and then calculates a customer's total cost of all orders as `quantity * unit_price` for as many orders a customer has. This transformed data is then loaded into a csv file.

> The `etl-alt.py` script invokes the `/customers` endpoint by passing through the desired status into the payload and transforms and outputs the data much the same as `etl.py`

This creates a pipeline where raw JSON data is loaded into a structured relational database, made accessible through an API, and then transformed into a csv file.

## What would I improve?

- I feel within the constraints of the task, I wouldn't improve/can't improve much on what is here, I feel I satisfied the requirements. However, I would've liked to flesh out this scenario and add more endpoints and querying on the existing `/customers` endpoint and more data. Though this has inspired me to tackle on a couple more projects.
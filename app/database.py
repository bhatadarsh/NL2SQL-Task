import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        amount REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_name TEXT,
        price REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );
    """)

    conn.commit()
    conn.close()


def insert_dummy_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data (for repeated runs)
    cursor.execute("DELETE FROM products;")
    cursor.execute("DELETE FROM orders;")
    cursor.execute("DELETE FROM customers;")

    # Insert customers
    customers = [
        (1, "John", "john@example.com"),
        (2, "Alice", "alice@example.com"),
        (3, "Bob", "bob@example.com")
    ]

    cursor.executemany("INSERT INTO customers VALUES (?, ?, ?);", customers)

    # Insert orders
    orders = [
        (1, 1, "2023-01-10", 500.0),
        (2, 1, "2023-02-15", 300.0),
        (3, 2, "2023-03-20", 700.0)
    ]

    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?);", orders)

    # Insert products
    products = [
        (1, 1, "Laptop", 500.0),
        (2, 2, "Mouse", 300.0),
        (3, 3, "Phone", 700.0)
    ]

    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?);", products)

    conn.commit()
    conn.close()
def execute_query(sql_query):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        conn.close()
        return column_names, results

    except Exception as e:
        conn.close()
        return None, str(e)

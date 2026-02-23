import sqlite3

DB_NAME = "database.db"


# -------------------------------
# Connection
# -------------------------------

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# -------------------------------
# Initialize Database (Full Schema)
# -------------------------------

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Temporarily disable foreign keys for reset
    cursor.execute("PRAGMA foreign_keys = OFF;")

    cursor.executescript("""
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;
    """)

    # Re-enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # ---------------- Customers ----------------
    cursor.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        city TEXT,
        country TEXT,
        signup_date TEXT,
        status TEXT,
        loyalty_points INTEGER
    );
    """)

    # ---------------- Products ----------------
    cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        brand TEXT,
        price REAL,
        cost_price REAL,
        stock_quantity INTEGER,
        rating REAL,
        created_at TEXT
    );
    """)

    # ---------------- Orders ----------------
    cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        shipping_date TEXT,
        delivery_date TEXT,
        total_amount REAL,
        discount_amount REAL,
        payment_method TEXT,
        order_status TEXT,
        shipping_city TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    """)

    # ---------------- Order Items ----------------
    cursor.execute("""
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        total_price REAL,
        tax_amount REAL,
        discount_amount REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)

    conn.commit()
    conn.close()


# -------------------------------
# Insert Dummy Data
# -------------------------------

def insert_dummy_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear previous data
    cursor.execute("DELETE FROM order_items;")
    cursor.execute("DELETE FROM orders;")
    cursor.execute("DELETE FROM products;")
    cursor.execute("DELETE FROM customers;")

    # ---------------- Customers ----------------
    customers = [
        (1, "John", "Doe", "john@example.com", "9876543210", "Delhi", "India", "2023-01-01", "Active", 120),
        (2, "Alice", "Smith", "alice@example.com", "9876543211", "Mumbai", "India", "2023-02-15", "Active", 200),
        (3, "Bob", "Brown", "bob@example.com", "9876543212", "Bangalore", "India", "2023-03-10", "Inactive", 50)
    ]

    cursor.executemany("""
    INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, customers)

    # ---------------- Products ----------------
    products = [
        (1, "Laptop", "Electronics", "Dell", 60000, 50000, 20, 4.5, "2023-01-05"),
        (2, "Phone", "Electronics", "Samsung", 30000, 25000, 50, 4.3, "2023-01-10"),
        (3, "Headphones", "Accessories", "Sony", 5000, 3500, 100, 4.6, "2023-02-01"),
        (4, "Keyboard", "Accessories", "Logitech", 2000, 1200, 75, 4.2, "2023-02-05")
    ]

    cursor.executemany("""
    INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products)

    # ---------------- Orders ----------------
    orders = [
        (1, 1, "2023-03-01", "2023-03-02", "2023-03-05", 65000, 5000, "Card", "Delivered", "Delhi"),
        (2, 2, "2023-03-10", "2023-03-11", "2023-03-14", 30000, 0, "UPI", "Delivered", "Mumbai"),
        (3, 1, "2023-04-01", "2023-04-02", "2023-04-05", 2000, 0, "COD", "Pending", "Delhi")
    ]

    cursor.executemany("""
    INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, orders)

    # ---------------- Order Items ----------------
    order_items = [
        (1, 1, 1, 1, 60000, 60000, 3000, 2000),
        (2, 1, 3, 1, 5000, 5000, 250, 0),
        (3, 2, 2, 1, 30000, 30000, 1500, 0),
        (4, 3, 4, 1, 2000, 2000, 100, 0)
    ]

    cursor.executemany("""
    INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, order_items)

    conn.commit()
    conn.close()


# -------------------------------
# Execute Query
# -------------------------------

def execute_query(sql_query):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()

        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]
        else:
            column_names = []

        conn.close()
        return column_names, results

    except Exception as e:
        conn.close()
        return None, str(e)
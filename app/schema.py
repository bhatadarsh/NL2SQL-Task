SCHEMA = {
    "customers": {
        "columns": {
            "customer_id": {"type": "INTEGER", "description": "Primary key"},
            "name": {"type": "VARCHAR", "description": "Customer name"},
            "email": {"type": "VARCHAR", "description": "Customer email"}
        },
        "primary_key": "customer_id",
        "foreign_keys": {}
    },
    "orders": {
        "columns": {
            "order_id": {"type": "INTEGER", "description": "Primary key"},
            "customer_id": {"type": "INTEGER", "description": "FK to customers"},
            "order_date": {"type": "DATE", "description": "Order date"},
            "amount": {"type": "FLOAT", "description": "Order amount"}
        },
        "primary_key": "order_id",
        "foreign_keys": {
            "customer_id": "customers.customer_id"
        }
    },
    "products": {
        "columns": {
            "product_id": {"type": "INTEGER", "description": "Primary key"},
            "order_id": {"type": "INTEGER", "description": "FK to orders"},
            "product_name": {"type": "VARCHAR", "description": "Product name"},
            "price": {"type": "FLOAT", "description": "Product price"}
        },
        "primary_key": "product_id",
        "foreign_keys": {
            "order_id": "orders.order_id"
        }
    }
}
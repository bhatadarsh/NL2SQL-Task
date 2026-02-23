SCHEMA = {
    "customers": {
        "columns": {
            "customer_id": {"type": "INTEGER"},
            "first_name": {"type": "VARCHAR"},
            "last_name": {"type": "VARCHAR"},
            "email": {"type": "VARCHAR"},
            "phone": {"type": "VARCHAR"},
            "city": {"type": "VARCHAR"},
            "country": {"type": "VARCHAR"},
            "signup_date": {"type": "DATE"},
            "status": {"type": "VARCHAR"},
            "loyalty_points": {"type": "INTEGER"}
        },
        "primary_key": "customer_id",
        "foreign_keys": {}
    },

    "products": {
        "columns": {
            "product_id": {"type": "INTEGER"},
            "product_name": {"type": "VARCHAR"},
            "category": {"type": "VARCHAR"},
            "brand": {"type": "VARCHAR"},
            "price": {"type": "FLOAT"},
            "cost_price": {"type": "FLOAT"},
            "stock_quantity": {"type": "INTEGER"},
            "rating": {"type": "FLOAT"},
            "created_at": {"type": "DATE"}
        },
        "primary_key": "product_id",
        "foreign_keys": {}
    },

    "orders": {
        "columns": {
            "order_id": {"type": "INTEGER"},
            "customer_id": {"type": "INTEGER"},
            "order_date": {"type": "DATE"},
            "shipping_date": {"type": "DATE"},
            "delivery_date": {"type": "DATE"},
            "total_amount": {"type": "FLOAT"},
            "discount_amount": {"type": "FLOAT"},
            "payment_method": {"type": "VARCHAR"},
            "order_status": {"type": "VARCHAR"},
            "shipping_city": {"type": "VARCHAR"}
        },
        "primary_key": "order_id",
        "foreign_keys": {
            "customer_id": "customers.customer_id"
        }
    },

    "order_items": {
        "columns": {
            "order_item_id": {"type": "INTEGER"},
            "order_id": {"type": "INTEGER"},
            "product_id": {"type": "INTEGER"},
            "quantity": {"type": "INTEGER"},
            "unit_price": {"type": "FLOAT"},
            "total_price": {"type": "FLOAT"},
            "tax_amount": {"type": "FLOAT"},
            "discount_amount": {"type": "FLOAT"}
        },
        "primary_key": "order_item_id",
        "foreign_keys": {
            "order_id": "orders.order_id",
            "product_id": "products.product_id"
        }
    }
}
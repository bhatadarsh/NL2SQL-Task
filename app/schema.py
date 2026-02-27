SCHEMA = {

    "customers": {
        "table_name": "bigquery-public-data.thelook_ecommerce.users",
        "columns": {
            "id": {"type": "INTEGER"},
            "first_name": {"type": "STRING"},
            "last_name": {"type": "STRING"},
            "email": {"type": "STRING"},
            "city": {"type": "STRING"},
            "country": {"type": "STRING"},
            "created_at": {"type": "TIMESTAMP"}
        },
        "primary_key": "id",
        "foreign_keys": {}
    },

    "products": {
        "table_name": "bigquery-public-data.thelook_ecommerce.products",
        "columns": {
            "id": {"type": "INTEGER"},
            "name": {"type": "STRING"},
            "category": {"type": "STRING"},
            "brand": {"type": "STRING"},
            "retail_price": {"type": "FLOAT"}
        },
        "primary_key": "id",
        "foreign_keys": {}
    },

    "orders": {
        "table_name": "bigquery-public-data.thelook_ecommerce.orders",
        "columns": {
            "order_id": {"type": "INTEGER"},
            "user_id": {"type": "INTEGER"},
            "status": {"type": "STRING"},
            "created_at": {"type": "TIMESTAMP"}
        },
        "primary_key": "order_id",
        "foreign_keys": {
            "user_id": "customers.id"
        }
    },

    "order_items": {
        "table_name": "bigquery-public-data.thelook_ecommerce.order_items",
        "columns": {
            "id": {"type": "INTEGER"},
            "order_id": {"type": "INTEGER"},
            "product_id": {"type": "INTEGER"},
            "sale_price": {"type": "FLOAT"},
            "created_at": {"type": "TIMESTAMP"}
        },
        "primary_key": "id",
        "foreign_keys": {
            "order_id": "orders.order_id",
            "product_id": "products.id"
        }
    }
}

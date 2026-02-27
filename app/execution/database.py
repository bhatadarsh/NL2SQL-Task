from app.config import USE_BIGQUERY

if USE_BIGQUERY:
    from .bigquery_db import execute_query
else:
    from .sqlite_db import execute_query

import re
from app.schema import SCHEMA


def clean_sql(sql: str) -> str:
    sql = sql.strip()
    sql = sql.replace("```sql", "").replace("```", "")
    sql = sql.strip()

    if not sql.endswith(";"):
        sql += ";"

    return sql


def extract_tables(sql):
    tables = re.findall(r'FROM\s+(\w+)|JOIN\s+(\w+)', sql, re.IGNORECASE)
    return {t for pair in tables for t in pair if t}


def extract_columns(sql):
    match = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE)
    if not match:
        return set()

    columns = match.group(1)
    columns = re.sub(r'\b(SUM|COUNT|AVG|MIN|MAX)\s*\(', '', columns, flags=re.IGNORECASE)
    columns = columns.replace(')', '')

    return {col.strip().split('.')[-1].split(" AS ")[0].strip()
            for col in columns.split(",")}


def validate_sql(sql: str):
    tables = extract_tables(sql)
    columns = extract_columns(sql)

    for table in tables:
        if table not in SCHEMA:
            return False, f"Invalid table: {table}"

    valid_columns = set()
    for table in tables:
        valid_columns.update(SCHEMA[table]["columns"].keys())

    for column in columns:
        if column != "*" and column not in valid_columns:
            return False, f"Invalid column: {column}"

    return True, "Valid SQL"
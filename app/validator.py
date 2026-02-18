import re
from app.schema import SCHEMA


def clean_sql(sql):
    sql = sql.strip()
    sql = sql.replace("sql", "")
    sql = sql.replace("", "")
    sql = sql.strip()

    if ";" in sql:
        sql = sql.split(";")[0] + ";"

    return sql


def extract_tables(sql):
    tables = re.findall(r'FROM\s+(\w+)|JOIN\s+(\w+)', sql, re.IGNORECASE)
    return {t for pair in tables for t in pair if t}


def extract_columns(sql):
    select_part = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE)
    if not select_part:
        return set()

    raw_columns = select_part.group(1)

    raw_columns = re.sub(r'\b(SUM|COUNT|AVG|MIN|MAX)\s*\(', '', raw_columns, flags=re.IGNORECASE)
    raw_columns = raw_columns.replace(')', '')

    columns = raw_columns.split(',')

    clean_columns = set()

    for col in columns:
        col = col.strip()

        if " AS " in col.upper():
            col = col.split(" AS ")[0].strip()

        if "." in col:
            col = col.split(".")[-1]

        clean_columns.add(col)

    return clean_columns


def validate_sql(sql):

    tables = extract_tables(sql)
    columns = extract_columns(sql)

    # Validate tables
    for table in tables:
        if table not in SCHEMA:
            return False, f"Invalid table: {table}"

    # Collect valid columns from used tables
    valid_columns = set()
    for table in tables:
        valid_columns.update(SCHEMA[table]["columns"].keys())

    # Validate columns
    for column in columns:
        if column != "*" and column not in valid_columns:
            return False, f"Invalid column: {column}"

    return True, "Valid SQL"
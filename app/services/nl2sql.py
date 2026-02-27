import re

from app.llm.prompts import SQL_PROMPT
from app.llm.gemini_client import ask_llm
from app.execution.database import execute_query
from app.validation.validator import validate_sql
from app.schema import SCHEMA
from app.config import DEFAULT_LIMIT


# -----------------------------
# Extract SQL from LLM output
# -----------------------------
def extract_sql(text):

    if not text:
        return ""

    text = text.replace("```sql", "").replace("```", "")

    match = re.search(r"(SELECT[\s\S]*)", text, re.IGNORECASE)

    if match:
        sql = match.group(1)
    else:
        sql = text

    return sql.strip()


# -----------------------------
# Map logical tables → BigQuery
# -----------------------------
def map_tables(sql):

    for logical, meta in SCHEMA.items():

        real = meta.get("table_name")

        if real:
            sql = re.sub(rf"\b{logical}\b", real, sql)

    return sql


# -----------------------------
# Add ORDER BY for analytics
# -----------------------------
def enforce_order(sql):

    sql_lower = sql.lower()

    if "avg(" in sql_lower or "sum(" in sql_lower or "count(" in sql_lower:

        if "order by" not in sql_lower:

            # try to detect alias
            alias_match = re.search(r"as\s+(\w+)", sql, re.IGNORECASE)

            if alias_match:
                metric = alias_match.group(1)
            else:
                metric = None

            if metric:
                sql += f" ORDER BY {metric} DESC"

    return sql


# -----------------------------
# Fix LIMIT safely
# -----------------------------
def enforce_limit(sql):

    sql = sql.strip()

    if sql.endswith(";"):
        sql = sql[:-1]

    if "limit" not in sql.lower():
        sql += f" LIMIT {DEFAULT_LIMIT}"

    return sql


# -----------------------------
# Main Pipeline
# -----------------------------
def run_pipeline(question):

    if not question:
        return {"error": "Question is empty"}

    prompt = SQL_PROMPT.format(question=question)

    raw_response = ask_llm(prompt)

    sql = extract_sql(raw_response)

    if not sql:
        return {"error": "Model did not return SQL"}

    if not validate_sql(sql):
        return {"error": "Invalid SQL generated"}

    sql = map_tables(sql)

    sql = enforce_order(sql)

    sql = enforce_limit(sql)

    columns, rows = execute_query(sql)

    if columns is None:
        return {
            "error": "Query execution failed",
            "sql": sql,
            "details": rows
        }

    return {
        "sql": sql,
        "columns": columns,
        "rows": rows
    }

import json
from app.prompts import get_intent_extraction_prompt, get_sql_generation_prompt
from app.gemini_client import call_gemini
from app.schema import SCHEMA
from app.validator import validate_sql, clean_sql
from app.database import execute_query


def generate_sql_from_question(question):

    # -------- Stage 1: Extract Intent --------
    intent_prompt = get_intent_extraction_prompt(question, SCHEMA)
    intent_raw = call_gemini(intent_prompt)

    try:
        intent = json.loads(intent_raw)
    except:
        return "Failed to parse intent JSON."

    if not intent.get("relevant"):
        tables = ", ".join(SCHEMA.keys())
        return f"Please ask questions related to these tables: {tables}"

    # -------- Stage 2: Generate SQL --------
    sql_prompt = get_sql_generation_prompt(intent, SCHEMA)
    sql_query = call_gemini(sql_prompt)

    # Clean SQL
    sql_query = clean_sql(sql_query)

    # -------- Validation --------
    valid, message = validate_sql(sql_query)

    if not valid:
        return f"Validation Failed: {message}"

    # -------- Execute Query --------
    columns, results = execute_query(sql_query)

    if columns is None:
        return f"Execution Error: {results}"

    output = f"Generated SQL:\n{sql_query}\n\nResults:\n"

    if not results:
        output += "No records found."
    else:
        output += str(columns) + "\n"
        for row in results:
            output += str(row) + "\n"

    return output

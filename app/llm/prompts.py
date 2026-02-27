from app.schema import SCHEMA

schema_text = ""

for table, meta in SCHEMA.items():
    cols = ", ".join(meta["columns"].keys())
    schema_text += f"\nTable: {table}\nColumns: {cols}\n"


SQL_PROMPT = f"""
You are an expert data analyst.

Database Schema:
{schema_text}

Rules:
Return ONLY SQL.
No explanations.
No markdown.
No comments.

Question:
{{question}}

SQL:
"""

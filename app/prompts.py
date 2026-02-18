
def get_intent_extraction_prompt(question, schema):
    return f"""
You are an expert system that converts natural language into structured JSON intent.

Available database schema:
{schema}

Return JSON in this exact format:

{{
  "relevant": true/false,
  "tables": [],
  "columns": [],
  "joins": [],
  "filters": [],
  "aggregations": []
}}

Rules:
- If question is unrelated to schema, set relevant=false.
- Only use tables and columns that exist in schema.
- Return ONLY valid JSON.
- Do not add explanation.

Question:
{question}
"""


def get_sql_generation_prompt(intent, schema):
    return f"""
You are a SQL generator.

Intent:
{intent}

Schema:
{schema}

Rules:
- Generate ONLY a valid SQL SELECT query.
- Use only tables and columns present in schema.
- Do NOT include explanation.
- Do NOT include markdown.
- Return raw SQL only.
"""


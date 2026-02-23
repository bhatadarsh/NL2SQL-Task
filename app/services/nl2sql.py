import json
import re
import time
import pandas as pd

from app.schema import SCHEMA
from app.llm.prompts import get_intent_extraction_prompt, get_sql_generation_prompt
from app.llm.gemini_client import call_gemini
from app.validation.validator import clean_sql, validate_sql
from app.execution.database import execute_query
from app.visualization.chart_selector import select_chart
from app.visualization.plotter import plot_bar, plot_line, plot_scatter


# =====================================================
# LLM RETRY MECHANISM
# =====================================================
def call_llm_with_retry(prompt, max_retries=2, base_delay=1):
    """
    Calls Gemini with retry mechanism and exponential backoff.
    """
    for attempt in range(max_retries + 1):
        try:
            response = call_gemini(prompt)

            if not response or response.strip() == "":
                raise ValueError("Empty LLM response")

            return response

        except Exception as e:
            if attempt == max_retries:
                raise e

            sleep_time = base_delay * (2 ** attempt)
            time.sleep(sleep_time)

    return None


# =====================================================
# SAFE JSON EXTRACTION
# =====================================================
def extract_json_safely(raw_text: str):
    """
    Extracts first JSON object from LLM output.
    Handles markdown fences and extra commentary.
    """
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON found in LLM output.")

    return json.loads(match.group())


# =====================================================
# JOIN GRAPH BUILDER
# =====================================================
def build_join_graph():
    graph = {}

    for table, meta in SCHEMA.items():
        graph.setdefault(table, set())

        for fk_field, ref in meta.get("foreign_keys", {}).items():
            ref_table = ref.split(".")[0]
            graph[table].add(ref_table)
            graph.setdefault(ref_table, set()).add(table)

    return graph


JOIN_GRAPH = build_join_graph()


def tables_can_be_joined(tables):
    if len(tables) <= 1:
        return True

    visited = set()

    def dfs(table):
        visited.add(table)
        for neighbor in JOIN_GRAPH.get(table, []):
            if neighbor not in visited:
                dfs(neighbor)

    dfs(tables[0])

    return all(table in visited for table in tables)


# =====================================================
# SMART SUGGESTIONS
# =====================================================
def generate_suggestions(tables):

    if not tables:
        return [
            "Show all customers",
            "Show all products",
            "Show total sales per product",
            "Show customers along with products they purchased"
        ]

    suggestions = []

    if "customers" in tables and "products" in tables:
        suggestions.append("Show customers along with products they purchased")
        suggestions.append("Show all customers")
        suggestions.append("Show all products")

    elif len(tables) > 1:
        for table in tables:
            suggestions.append(f"Show all {table}")

    else:
        suggestions.append(f"Show all {tables[0]}")

    return suggestions


# =====================================================
# MAIN PIPELINE
# =====================================================
def process_question(question: str):

    # -------- Stage 1: Intent Extraction --------
    intent_prompt = get_intent_extraction_prompt(question, SCHEMA)

    try:
        intent_raw = call_llm_with_retry(intent_prompt)
        intent = extract_json_safely(intent_raw)
    except Exception:
        return {
            "error": "I couldn't fully understand your request.",
            "suggestions": generate_suggestions([])
        }

    if not intent.get("relevant"):
        return {
            "error": "Your question is not related to the available database.",
            "suggestions": generate_suggestions([])
        }

    tables = intent.get("tables", [])

    # -------- Stage 2: Join Validation --------
    if not tables_can_be_joined(tables):
        return {
            "error": "Your question references tables that are not directly related.",
            "suggestions": generate_suggestions(tables)
        }

    # -------- Stage 3: SQL Generation --------
    sql_prompt = get_sql_generation_prompt(intent, SCHEMA)

    try:
        sql_raw = call_llm_with_retry(sql_prompt)
        sql_query = clean_sql(sql_raw)
    except Exception:
        return {
            "error": "LLM failed while generating SQL.",
            "suggestions": generate_suggestions(tables)
        }

    # -------- Stage 4: SQL Validation --------
    valid, message = validate_sql(sql_query)

    if not valid:
        # Retry once with stricter instruction
        retry_prompt = sql_prompt + "\nIMPORTANT: Ensure all columns and tables strictly exist in the schema."

        try:
            retry_sql_raw = call_llm_with_retry(retry_prompt)
            retry_sql_query = clean_sql(retry_sql_raw)

            retry_valid, retry_message = validate_sql(retry_sql_query)

            if retry_valid:
                sql_query = retry_sql_query
            else:
                return {
                    "error": f"Generated SQL was invalid after retry: {retry_message}",
                    "suggestions": generate_suggestions(tables)
                }

        except Exception:
            return {
                "error": "LLM failed while retrying SQL generation.",
                "suggestions": generate_suggestions(tables)
            }

    # -------- Stage 5: Execution --------
    columns, results = execute_query(sql_query)

    if columns is None:
        return {
            "error": f"Database execution error: {results}"
        }

    df = pd.DataFrame(results, columns=columns)

    # -------- Stage 6: Visualization --------
    chart_type = select_chart(columns, results)
    chart = None

    if chart_type == "bar":
        chart = plot_bar(columns, results)

    elif chart_type == "line":
        chart = plot_line(columns, results)

    elif chart_type == "scatter":
        chart = plot_scatter(columns, results)

    return {
        "sql": sql_query,
        "data": df,
        "chart": chart
    }
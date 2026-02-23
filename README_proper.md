# NL2SQL Intelligent Analytics Engine

A modular Natural Language to SQL analytics system that converts plain
English questions into validated SQL queries, executes them on a
relational database, and automatically generates analytical
visualizations.

Unlike simple prompt-to-SQL demos, this project focuses on LLM system
design with guardrails, validation layers, and structured reasoning.

------------------------------------------------------------------------

# Overview

Business users frequently need insights from databases but do not know
SQL.

This project enables users to ask questions like:

**Show total sales per product**

and automatically receive:

-   Correct SQL query
-   Database results
-   Analytical visualization

while ensuring:

-   Safety
-   Accuracy
-   Reliability
-   Explainability

------------------------------------------------------------------------

# Key Features

## Natural Language Querying

Users can interact with a database using plain English.

## Intent Extraction Layer

Queries are converted into structured JSON before SQL generation.

## Schema Grounding

The system only generates queries using known tables and columns.

## SQL Guardrails

Queries are validated before execution to prevent hallucinations.

## Automatic Visualization

Results are automatically visualized using appropriate chart types.

## Retry & Error Handling

LLM failures are handled with structured retry logic.

## Modular Architecture

Each component (LLM, validation, execution, visualization) is isolated.

------------------------------------------------------------------------

# System Architecture

    User (Streamlit UI)
            │
            ▼
    Service Layer (nl2sql.py)
            │
            ▼
    Intent Extraction (LLM)
            │
            ▼
    Intent Validation
            │
            ▼
    SQL Generation (LLM)
            │
            ▼
    SQL Guardrails
            │
            ▼
    Database Execution
            │
            ▼
    Result Structuring
            │
            ▼
    Visualization Engine
            │
            ▼
    Response to User

------------------------------------------------------------------------

# End-to-End Workflow

## 1. User Input

The user submits a question in natural language.

Example:

    Show total sales per product

The request can be submitted via:

-   Streamlit UI
-   Command line interface

------------------------------------------------------------------------

## 2. Intent Extraction

Instead of generating SQL directly, the system first extracts a
structured intent representation using the LLM.

Example:

``` json
{
  "relevant": true,
  "tables": ["products", "order_items"],
  "columns": ["product_name"],
  "aggregations": ["SUM(total_price)"]
}
```

### Why this matters

This step:

-   Reduces hallucinated tables
-   Improves reasoning
-   Makes debugging easier
-   Adds transparency to the pipeline

------------------------------------------------------------------------

## 3. JSON Safety Layer

LLMs sometimes return malformed JSON.

The system stabilizes responses by:

-   Removing markdown wrappers
-   Extracting valid JSON
-   Retrying generation if parsing fails

This ensures the pipeline continues without breaking.

------------------------------------------------------------------------

## 4. Join Relationship Validation

Using metadata from the schema, the system builds a join graph based on
foreign keys.

Example relationship chain:

    customers → orders → order_items → products

If a query references unrelated tables, the system:

-   Suggests valid alternatives
-   Prevents invalid joins

------------------------------------------------------------------------

## 5. SQL Generation

The validated intent and schema are sent to the LLM to generate SQL.

Example:

``` sql
SELECT p.product_name, SUM(oi.total_price)
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_name;
```

------------------------------------------------------------------------

## 6. SQL Validation Layer

Before execution, SQL is validated against the schema.

Checks include:

-   Table existence
-   Column existence
-   Join validity
-   Query structure

This prevents:

-   Hallucinated columns
-   Broken joins
-   Unsafe queries

------------------------------------------------------------------------

## 7. Retry Mechanism

LLM calls can fail due to:

-   API errors
-   Network issues
-   Formatting mistakes

The system retries with exponential backoff.

Example:

    Attempt 1 → wait 1 second
    Attempt 2 → wait 2 seconds
    Attempt 3 → fail gracefully

If SQL validation fails, the system retries generation with stricter
prompts.

------------------------------------------------------------------------

## 8. Query Execution

Validated SQL is executed on a SQLite database.

Results returned include:

-   Column names
-   Row data

These results are converted into a Pandas DataFrame for further
processing.

------------------------------------------------------------------------

## 9. Automatic Visualization

The system automatically determines the best visualization based on the
data structure.

  Data Pattern         Visualization
  -------------------- ---------------
  Category + Numeric   Bar Chart
  Date + Numeric       Line Chart
  Numeric + Numeric    Scatter Plot

Example:

    product_name + total_sales

→ Bar chart is generated automatically.

------------------------------------------------------------------------

# Project Structure

    nl2sql_gemini/
    │
    ├── app/
    │   ├── config.py
    │   ├── schema.py
    │   │
    │   ├── services/
    │   │      nl2sql.py
    │   │
    │   ├── llm/
    │   │      gemini_client.py
    │   │      prompts.py
    │   │
    │   ├── execution/
    │   │      database.py
    │   │
    │   ├── validation/
    │   │      validator.py
    │   │
    │   └── visualization/
    │          chart_selector.py
    │          plotter.py
    │
    ├── streamlit_app.py
    ├── main.py
    └── README.md

------------------------------------------------------------------------

# Module Responsibilities

## schema.py

Defines database structure:

-   Tables
-   Columns
-   Foreign key relationships

This prevents the LLM from inventing schema elements.

## prompts.py

Contains prompt templates used for:

-   Intent extraction
-   SQL generation
-   Error correction

Centralizing prompts makes experimentation easier.

## gemini_client.py

Handles communication with the Google Gemini API:

-   API calls
-   Retry logic
-   Response cleaning

## validator.py

Responsible for SQL safety checks:

-   Valid tables
-   Valid columns
-   Join validation
-   Query structure checks

## database.py

Handles database interaction:

-   Query execution
-   Result fetching
-   Conversion to DataFrame

## chart_selector.py

Analyzes result structure and decides which chart type to generate.

## plotter.py

Uses Matplotlib to render charts.

## nl2sql.py

The main orchestration layer that connects:

-   LLM
-   Validation
-   Execution
-   Visualization

## streamlit_app.py

Provides a simple user interface where users can:

-   Enter questions
-   View SQL
-   See results
-   Explore charts

------------------------------------------------------------------------

# Installation

## 1. Clone Repository

    git clone <repository-url>
    cd nl2sql_gemini

## 2. Create Virtual Environment

Linux / Mac:

    python3 -m venv venv
    source venv/bin/activate

Windows:

    venv\Scriptsctivate

## 3. Install Dependencies

    pip install pandas matplotlib streamlit google-generativeai

Optional:

    pip install python-dotenv

## 4. Configure API Key

Set your Google Gemini API key.

Linux / Mac:

    export GEMINI_API_KEY="your_api_key"

Windows:

    set GEMINI_API_KEY=your_api_key

Or store it inside config.py.

------------------------------------------------------------------------

# Running the Application

## Streamlit Interface

    streamlit run streamlit_app.py

Open:

    http://localhost:8501

## CLI Mode

You can also run the engine from the terminal:

    python main.py

Example interaction:

    Enter your question: Show total sales per product

------------------------------------------------------------------------

# Example Queries

-   Show all customers
-   Show all products
-   Show total sales per product
-   Show customers with highest loyalty points
-   Show orders from last month

------------------------------------------------------------------------

# Example Output

### User Query

Show total sales per product

### Generated SQL

``` sql
SELECT p.product_name, SUM(oi.total_price)
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_name;
```

### Output

-   Table of results
-   Bar chart visualization

------------------------------------------------------------------------

# Challenges Addressed

## LLM Hallucination

Prevented using schema grounding and validation.

## SQL Safety

Queries validated before execution.

## Ambiguous Queries

Intent layer improves reasoning.

## Robustness

Retries and JSON repair mechanisms stabilize LLM output.

## Visualization Automation

Charts generated without manual selection.

------------------------------------------------------------------------

# Future Improvements

-   Interactive charts with Plotly
-   Query caching
-   Conversation memory
-   Multi-database support
-   Authentication and user roles
-   Advanced prompt optimization
-   Query explanation for non-technical users

------------------------------------------------------------------------

# Technologies Used

-   Python
-   SQLite
-   Streamlit
-   Google Gemini API
-   Pandas
-   Matplotlib

------------------------------------------------------------------------

# Author

Adarsh Bhavimane

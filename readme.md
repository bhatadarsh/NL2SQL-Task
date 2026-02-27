# 🚀 AI Cloud Data Analyst

### Natural Language Analytics with LLM + BigQuery

An intelligent analytics system that allows users to query cloud
datasets using natural language.\
The platform converts questions into SQL using a Large Language Model,
executes queries on **Google BigQuery**, generates visualizations, and
produces AI-powered insights.

------------------------------------------------------------------------

# 📌 Project Overview

Modern organizations store large volumes of data in cloud warehouses,
but accessing insights often requires SQL expertise.

This project enables:

**Natural Language → SQL → Insights**

Example:

    Show average product price by category

The system automatically:

-   Generates SQL using an LLM
-   Runs the query on BigQuery
-   Builds charts
-   Produces business insights

------------------------------------------------------------------------

# 🧠 Core Capabilities

✔ Natural Language Querying\
✔ LLM-powered SQL generation\
✔ BigQuery cloud analytics\
✔ Automatic visualization\
✔ AI-generated insights\
✔ Query safety guardrails\
✔ Modern dashboard UI

------------------------------------------------------------------------

# 🏗 System Architecture

``` mermaid
flowchart TD

A[User Question] --> B[Streamlit Interface]
B --> C[NL2SQL Engine - Gemini LLM]
C --> D[SQL Validation Layer]
D --> E[BigQuery Execution]
E --> F[Pandas Data Processing]
F --> G[Visualization Engine]
G --> H[AI Insight Generator]
H --> I[Interactive Dashboard]
```

------------------------------------------------------------------------

# ⚙️ End-to-End Workflow

## 1. User Question

The user asks a natural language question.

Example:

    Show average product price by category

------------------------------------------------------------------------

## 2. Schema Grounding

The system injects schema information into the prompt so the model
understands:

-   Available tables
-   Columns
-   Relationships

Example:

    products
    - id
    - category
    - retail_price

------------------------------------------------------------------------

## 3. SQL Generation (LLM)

The prompt is sent to **Google Gemini** which generates SQL.

Example:

``` sql
SELECT category, AVG(retail_price)
FROM products
GROUP BY category
```

------------------------------------------------------------------------

## 4. Query Optimization

The system improves the query by adding:

-   BigQuery dataset mapping
-   Sorting
-   LIMIT clause

Final SQL executed:

``` sql
SELECT category, AVG(retail_price) AS avg_price
FROM bigquery-public-data.thelook_ecommerce.products
GROUP BY category
ORDER BY avg_price DESC
LIMIT 100
```

------------------------------------------------------------------------

# ☁️ BigQuery Integration

Queries are executed using:

    google-cloud-bigquery

Advantages:

-   Serverless analytics
-   Petabyte scale
-   Distributed execution
-   Public datasets

------------------------------------------------------------------------

# 📊 Visualization Pipeline

The system automatically chooses the best chart type.

  Data Pattern         Chart
  -------------------- ------------
  Category + Numeric   Bar Chart
  Date + Numeric       Line Chart
  Small Groups         Pie Chart

Charts are rendered using **Plotly** for interactive dashboards.

------------------------------------------------------------------------

# 🤖 AI Insight Generation

After generating the visualization, the system sends the result preview
back to the LLM.

Example output:

-   Outerwear has the highest average price
-   Formalwear categories dominate premium segments
-   Essentials show lowest pricing

This simulates the reasoning of a **data analyst**.

------------------------------------------------------------------------

# 📦 Dataset

Public dataset used:

    bigquery-public-data.thelook_ecommerce

Contains:

-   Products
-   Orders
-   Customers
-   Prices
-   Categories

------------------------------------------------------------------------

# 🗂 Project Structure

    nl2sql_gemini/

    app/
    │
    ├── analysis/
    │   └── insights_generator.py
    │
    ├── execution/
    │   ├── bigquery_db.py
    │   ├── sqlite_db.py
    │   └── database.py
    │
    ├── llm/
    │   ├── gemini_client.py
    │   └── prompts.py
    │
    ├── services/
    │   └── nl2sql.py
    │
    ├── validation/
    │   └── validator.py
    │
    ├── visualization/
    │   ├── chart_selector.py
    │   └── plotter.py
    │
    ├── schema.py
    └── config.py

    streamlit_app.py
    main.py
    README.md

------------------------------------------------------------------------

# 🧰 Technologies

  Technology        Purpose
  ----------------- -----------------
  Python            Core system
  Streamlit         UI
  Gemini LLM        SQL + insights
  Google BigQuery   Data warehouse
  Pandas            Data processing
  Plotly            Visualization

------------------------------------------------------------------------

# 🚀 Installation

## Clone Repository

    git clone <repo-url>
    cd nl2sql_gemini

## Create Environment

    python3 -m venv venv
    source venv/bin/activate

## Install Dependencies

    pip install streamlit pandas plotly google-generativeai google-cloud-bigquery

------------------------------------------------------------------------

# 🔑 Configure API

Set Gemini API Key

    export GEMINI_API_KEY="your_api_key"

Authenticate BigQuery

    gcloud auth application-default login

------------------------------------------------------------------------

# ▶ Running the App

    streamlit run streamlit_app.py

Open:

    http://localhost:8501

------------------------------------------------------------------------

# 💬 Example Queries

-   Show average product price by category
-   Show revenue trend over time
-   Show number of products per category
-   Show product distribution
-   Show top 10 expensive categories

------------------------------------------------------------------------

# 📈 Example Output

User Question:

    Show average product price by category

System Generates:

-   SQL query
-   Interactive chart
-   AI insights
-   Data table

------------------------------------------------------------------------

# ⚠ Challenges Solved

### LLM Hallucination

Schema grounding ensures correct table usage.

### Query Safety

LIMIT clauses prevent large scans.

### Automation

Visualization and insights require no manual setup.

------------------------------------------------------------------------

# 🔮 Future Improvements

-   Conversational analytics
-   Query caching
-   Cost estimation
-   Multi-dataset support
-   Authentication
-   Dashboard mode

------------------------------------------------------------------------

# 👤 Author

Adarsh Bhavimane

------------------------------------------------------------------------

# ⭐ Summary

This project demonstrates how **LLMs + Cloud Data Warehouses** can
transform data exploration.

Traditional workflow:

    SQL → Charts → Insights

AI workflow:

    Question → Insights

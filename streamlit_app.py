import streamlit as st
import pandas as pd

from app.services.nl2sql import run_pipeline
from app.analysis.insights_generator import generate_insights
from app.visualization.plotter import plot_chart


# ---------------------------
# Page Config
# ---------------------------

st.set_page_config(
    page_title="AI Cloud Data Analyst",
    page_icon="📊",
    layout="wide"
)


# ---------------------------
# Custom Styling
# ---------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

h1 {
    font-weight: 700;
}

div[data-testid="stMetricValue"] {
    font-size: 28px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------
# Header
# ---------------------------

st.title("📊 AI Cloud Data Analyst")

st.write("Ask questions about cloud datasets and get instant analytics.")


# ---------------------------
# Input
# ---------------------------

question = st.text_input(
    "Ask a data question",
    placeholder="Example: Show average product price by category"
)


# ---------------------------
# Run Query
# ---------------------------

if st.button("Analyze", use_container_width=True):

    result = run_pipeline(question)

    if "error" in result:
        st.error(result["error"])

    else:

        df_columns = result["columns"]
        df_rows = result["rows"]

        df = pd.DataFrame(df_rows, columns=df_columns)

        # ---------------------------
        # KPI Row
        # ---------------------------

        k1, k2, k3 = st.columns(3)

        k1.metric("Rows Returned", len(df))
        k2.metric("Columns", len(df.columns))
        k3.metric("Dataset", "BigQuery Public Data")

        st.divider()

        # ---------------------------
        # Main Layout
        # ---------------------------

        col1, col2 = st.columns([2, 1])

        with col1:

            st.subheader("Visualization")

            fig = plot_chart(df_columns, df_rows)

            if fig:
                st.plotly_chart(fig, use_container_width=True)

        with col2:

            st.subheader("AI Insights")

            insights = generate_insights(df_columns, df_rows)

            for ins in insights:
                st.markdown(f"• {ins}")

        st.divider()

        # ---------------------------
        # Data Table
        # ---------------------------

        st.subheader("Data")

        st.dataframe(df, use_container_width=True)

        # ---------------------------
        # SQL
        # ---------------------------

        with st.expander("Generated SQL"):
            st.code(result["sql"])

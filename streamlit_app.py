import streamlit as st
from app.services.nl2sql import process_question

st.set_page_config(page_title="NL2SQL Dashboard", layout="wide")

st.title("💬 NL2SQL Intelligent Dashboard")

question = st.text_input("Ask your question about the data:")

if st.button("Run") and question:

    response = process_question(question)

    # -------- ERROR HANDLING --------
    if "error" in response:
        st.error(response["error"])

        # Suggestions if available
        if "suggestions" in response:
            st.subheader("Did you mean:")
            for suggestion in response["suggestions"]:
                if st.button(suggestion):
                    new_response = process_question(suggestion)

                    if "error" not in new_response:
                        st.subheader("Generated SQL")
                        st.code(new_response["sql"], language="sql")

                        st.subheader("Results")
                        st.dataframe(new_response["data"])

                        if new_response["chart"] is not None:
                            st.subheader("Visualization")
                            st.pyplot(new_response["chart"])

    # -------- SUCCESS --------
    else:
        st.subheader("Generated SQL")
        st.code(response["sql"], language="sql")

        st.subheader("Results")
        st.dataframe(response["data"])

        if response["chart"] is not None:
            st.subheader("Visualization")
            st.pyplot(response["chart"])
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Natural Language to SQL", layout="wide")

st.title("?? Natural Language to SQL (NL2SQL)")
st.markdown("Ask questions about the `employees` database in plain English.")

question = st.text_input("?? Ask your question:", "")

if question:
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:8000/ask",
            json={"question": question}
        ).json()

    if "error" in response:
        st.error(f"? Error: {response['error']}")
        st.code(response.get("sql", ""), language="sql")
    else:
        st.subheader("? SQL Query")
        st.code(response["sql"], language="sql")

        # Convert to DataFrame
        df = pd.DataFrame(response["rows"], columns=response["columns"])

        st.subheader("?? Data Table")
        st.dataframe(df)


    # Plotting
    if not df.empty:
        st.subheader("?? Optional: Visualize the Results")

        # Get numeric and text columns
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        all_cols = df.columns.tolist()

        if len(numeric_cols) >= 1 and len(all_cols) >= 2:
            chart_type = st.radio("Choose chart type", ["Bar", "Line"], horizontal=True)

            # Suggest first string column for x, and first numeric for y
            default_x = next((col for col in all_cols if col not in numeric_cols), all_cols[0])
            default_y = numeric_cols[0]

            x_axis = st.selectbox("X-axis", options=all_cols, index=all_cols.index(default_x))
            y_axis = st.selectbox("Y-axis (numeric only)", options=numeric_cols, index=0)

            # Check if selected columns exist
            if x_axis in df.columns and y_axis in df.columns:
                try:
                    plot_data = df[[x_axis, y_axis]].set_index(x_axis)
                    if chart_type == "Bar":
                        st.bar_chart(plot_data)
                    else:
                        st.line_chart(plot_data)
                except Exception as e:
                    st.warning(f"?? Could not generate chart: {e}")
            else:
                st.warning("?? Selected columns are not in the result.")
        else:
            st.info("?? To show a chart, ask a question that returns at least one numeric and one other column.")

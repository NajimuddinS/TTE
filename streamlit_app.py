import streamlit as st
from data_handler import parse_file_to_df, df_to_markdown_table
from llm_generator import get_schedule_summary

st.set_page_config(page_title="Timetable Summarizer", layout="wide")

# --- UI Header ---
st.title("📅 AI Timetable Summarizer")
st.markdown("Upload your class schedule (CSV, XLS, XLSX, or JSON) to get a comprehensive, chat-like summary.")

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "Choose a schedule file",
    type=['csv', 'xls', 'xlsx', 'json'],
    help="Ensure your file has clear columns like Day, Time, Subject, etc."
)

if uploaded_file is not None:
    # --- 1. Parsing and Standardization ---
    with st.spinner("Step 1/3: Reading and standardizing file data..."):
        df, error = parse_file_to_df(uploaded_file)

        if error:
            st.error(error)
            st.stop()

    st.success("File loaded successfully! Reviewing the raw data structure:")
    st.dataframe(df.head())

    # --- 2. Conversion to LLM Input Format ---
    markdown_data = df_to_markdown_table(df)

    # --- 3. Summarization and Response Generation ---
    if st.button("Generate AI Schedule Summary 🤖", type="primary"):
        with st.spinner("Step 3/3: Sending data to LLM and generating summary... (Powered by Groq)"):
            summary_text = get_schedule_summary(markdown_data)

            st.subheader("✅ AI Schedule Summary (Chat Response)")
            # Use a chat-style container for the final output
            with st.container(border=True):
                 st.markdown(summary_text)

            st.info("💡 **Tip:** If the summary is poor, check the 'Raw Data Sent to LLM' section to ensure column headers are clear (e.g., 'Mon', 'Start Time').")

    # --- Debugging/Transparency (Optional) ---
    with st.expander("Show Raw Data Sent to LLM"):
        st.code(markdown_data, language='markdown')
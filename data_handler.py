import pandas as pd
import io

def parse_file_to_df(uploaded_file):
    """Reads a file (csv, xls/xlsx, json) and returns a Pandas DataFrame."""
    try:
        # Determine file type
        file_type = uploaded_file.name.split('.')[-1].lower()

        # Read the file content into a byte stream
        data = uploaded_file.read()

        if file_type == 'csv':
            df = pd.read_csv(io.StringIO(data.decode('utf-8')))
        elif file_type in ['xls', 'xlsx']:
            # Use a byte stream for Excel files
            df = pd.read_excel(io.BytesIO(data))
        elif file_type == 'json':
            df = pd.read_json(io.StringIO(data.decode('utf-8')))
        else:
            return None, "Unsupported file format."

        # Basic cleaning and standardization: Drop fully empty columns/rows
        df.dropna(how='all', axis=1, inplace=True)
        df.dropna(how='all', axis=0, inplace=True)

        return df, None
    except Exception as e:
        return None, f"Error processing file: {e}"

def df_to_markdown_table(df):
    """Converts the DataFrame into a string-based Markdown table for the LLM."""
    if df is not None and not df.empty:
        # Fill NA values with an empty string for cleaner LLM input
        df_clean = df.fillna('')
        # Convert to Markdown format
        markdown_table = df_clean.to_markdown(index=False)
        return markdown_table
    return "The schedule data is empty or invalid."
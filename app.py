import streamlit as st
import pandas as pd

# Set page title and configuration
st.set_page_config(
    page_title="CSV Viewer & Filter",
    page_icon="📊",
    layout="wide"
)

# App title and description
st.title("📊 CSV Viewer & Filter")
st.write("Upload a CSV file, view it as a table, and filter by column values.")

# Initialize session state for the dataframe if it doesn't exist
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.filtered_df = df.copy()
        
        # Display basic info
        st.write("### Data Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Rows:** {df.shape[0]}")
        with col2:
            st.info(f"**Columns:** {df.shape[1]}")
        with col3:
            st.info(f"**Data types:** {len(df.dtypes.unique())}")
        
        # Filtering section
        st.write("### Filter Data")
        filter_col, filter_val_col, button_col = st.columns([2, 2, 1])
        
        with filter_col:
            filter_column = st.selectbox("Select column for filtering", options=df.columns)
        
        with filter_val_col:
            unique_values = df[filter_column].unique()
            if df[filter_column].dtype == 'object' or len(unique_values) < 10:
                # For categorical columns or columns with few unique values, show a selectbox
                filter_value = st.selectbox("Select value to filter by", options=[""] + list(unique_values))
            else:
                # For numerical columns with many values, use text input
                filter_value = st.text_input("Enter value to filter by (exact match)")
        
        with button_col:
            reset_button = st.button("Reset Filter")
            
        # Apply filtering
        if filter_value and not reset_button:
            # Convert input to the correct type if needed
            if df[filter_column].dtype != 'object' and filter_value:
                try:
                    if df[filter_column].dtype == 'int64':
                        filter_value = int(filter_value)
                    elif df[filter_column].dtype == 'float64':
                        filter_value = float(filter_value)
                except ValueError:
                    st.error(f"Input value '{filter_value}' cannot be converted to {df[filter_column].dtype}.")
                    filter_value = None
            
            if filter_value:
                filtered_df = df[df[filter_column] == filter_value]
                st.session_state.filtered_df = filtered_df
        elif reset_button:
            st.session_state.filtered_df = df.copy()
        
        # Display data table
        st.write("### Data Table")
        if st.session_state.filtered_df.empty:
            st.warning("No matching records found with the current filter.")
        else:
            st.dataframe(st.session_state.filtered_df, use_container_width=True)
            
            # Information about filtered results
            if st.session_state.filtered_df.shape[0] != df.shape[0]:
                st.success(f"Showing {st.session_state.filtered_df.shape[0]} out of {df.shape[0]} records after filtering.")
        
    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")
else:
    st.info("👆 Please upload a CSV file to get started.")
    
    # Example usage
    st.write("### Example")
    st.write("""
    1. Upload a CSV file using the file uploader above
    2. View the data in the table
    3. Select a column and enter a value to filter the data
    4. The table will update to show only rows where the column equals the value you entered
    5. Click 'Reset Filter' to show all data again
    """)
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import io
import warnings
warnings.filterwarnings('ignore')

def read_csv_file(uploaded_file):
    """Reads a CSV file from uploaded data and displays all rows."""
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("Data from the uploaded CSV:")
        st.dataframe(df)  # Display the entire DataFrame
        return df
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        return None

def get_columns(df):
    """Separates columns into numerical and categorical."""
    if df is None:
        return [], []
    numerical_columns = df.select_dtypes(include=np.number).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    return numerical_columns, categorical_columns

def create_bar_graph(df, x_col, y_col):
    """Creates a bar graph using Streamlit."""
    if df is None or x_col not in df.columns or y_col not in df.columns:
        st.error("Error: DataFrame is None or specified columns not found.")
        return
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_col], df[y_col])
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"Bar Graph of {y_col} by {x_col}")
    st.pyplot(plt)

def create_line_graph(df, x_col, y_col):
    """Creates a line graph using Streamlit."""
    if df is None or x_col not in df.columns or y_col not in df.columns:
        st.error("Error: DataFrame is None or specified columns not found.")
        return
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_col], df[y_col], marker='o')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"Line Graph of {y_col} by {x_col}")
    plt.grid(True)
    st.pyplot(plt)

def create_pie_chart(df, category_col, value_col):
    """Creates a pie chart using Streamlit."""
    if df is None or category_col not in df.columns or value_col not in df.columns:
        st.error("Error: DataFrame is None or specified columns not found.")
        return

    grouped_data = df.groupby(category_col)[value_col].sum()
    if grouped_data.sum() == 0:
        st.error("Error: The sum of values is zero. Cannot create a pie chart.")
        return

    plt.figure(figsize=(8, 8))
    plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=140)
    plt.title(f"Pie Chart of {value_col} by {category_col}")
    st.pyplot(plt)

def main():
    """Main function to execute the data analysis and plotting using Streamlit."""
    st.title("CSV Data Visualizer")
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

    if uploaded_file is not None:
        df = read_csv_file(uploaded_file)
        if df is not None:
            numerical_columns, categorical_columns = get_columns(df)
            if numerical_columns and categorical_columns:
                st.sidebar.header("Plot Settings")

                # Bar Chart
                st.sidebar.subheader("Bar Chart")
                bar_x_col = st.sidebar.selectbox("X-Axis", categorical_columns, key="bar_x")
                bar_y_col = st.sidebar.selectbox("Y-Axis", numerical_columns, key="bar_y")
                if st.sidebar.button("Generate Bar Chart"):
                    create_bar_graph(df, bar_x_col, bar_y_col)

                # Line Chart
                st.sidebar.subheader("Line Chart")
                line_x_col = st.sidebar.selectbox("X-Axis", numerical_columns, key="line_x")
                line_y_col = st.sidebar.selectbox("Y-Axis", numerical_columns, key="line_y")
                if st.sidebar.button("Generate Line Chart"):
                    create_line_graph(df, line_x_col, line_y_col)

                # Pie Chart
                st.sidebar.subheader("Pie Chart")
                pie_category_col = st.sidebar.selectbox("Category Column", categorical_columns, key="pie_cat")
                pie_value_col = st.sidebar.selectbox("Value Column", numerical_columns, key="pie_val")
                if st.sidebar.button("Generate Pie Chart"):
                    create_pie_chart(df, pie_category_col, pie_value_col)
            else:
                st.warning("Not enough suitable columns in the data to create plots.")
    else:
        st.info("Please upload a CSV file to begin.")

if __name__ == "__main__":
    main()